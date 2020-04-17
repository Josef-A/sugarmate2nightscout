"""
License:
GNU Affero General Public License (AGPLv3)

Author:
Josef Andersson April 2020

Github:

"""

import datetime
import hashlib
import msvcrt
import os
import sys
import time
import yaml
import requests
from pathlib import Path
import sugarmate2nightscout

# Constants

HOMEFOLDER = str(Path.home())

DEFAULT_CFG_FILE = 'sugarmate2nightscout.yaml'

DIRECTIONS = {
    0: 'NONE',
    1: 'DoubleUp',
    2: 'SingleUp',
    3: 'FortyFiveUp',
    4: 'Flat',
    5: 'FortyFiveDown',
    6: 'SingleDown',
    7: 'DoubleDown',
    8: 'NOT COMPUTABLE',
    9: 'RATE OUT OF RANGE'
}
# Default values
DEFAULT_CFG = {
    'sync_phase': 310,  # [Seconds] 5 min, 10 sec
    'retry_interval': 10  # 10 seconds
}


class NoConfigfile(Exception):
    """Could not find any configuration file"""


def check_cfg(cfg):
    assert 'sugarmate_url' in cfg, 'URL to sugarmate must be defined (sugarmate_url)'
    assert cfg['sugarmate_url'] is not None, 'URL to sugarmate must be defined (sugarmate_url)'
    assert len(cfg['sugarmate_url']) > 1, 'URL to sugarmate must be defined (sugarmate_url)'
    assert 'nightscout_url' in cfg, 'URL to Nightscout must be defined (nightscout_url)'
    assert cfg['nightscout_url'] is not None, 'URL to Nightscout must be defined (nightscout_url)'
    assert len(cfg['nightscout_url']) > 1, 'URL to Nightscout must be defined (nightscout_url)'
    assert 'api_secret' in cfg, 'API_secret to Nightscout must be defined (api_secret)'
    assert cfg['api_secret'] is not None, 'API_secret to Nightscout must be defined (api_secret)'
    assert len(cfg['api_secret']) > 1, 'API_secret to Nightscout must be defined (api_secret)'


def read_cfg():
    cfg_filename = get_cfg_filename()
    with open(cfg_filename, "r") as ymlfile:
        new_cfg = yaml.safe_load(ymlfile)
    # Check for mandatory fields
    check_cfg(new_cfg)

    # Fill in with default values
    cfg = DEFAULT_CFG.copy()
    cfg.update(new_cfg)

    return cfg


def read_sugarmate(cfg):
    # Read json from sugarmate
    sugarmate_response = requests.get(url=cfg['sugarmate_url'])
    if not sugarmate_response.ok:
        print('Something went wrong while reading from sugarmate')
        print(f'Response code {sugarmate_response.status_code}')
        print(f'Message\n{sugarmate_response.text}')
    sm = sugarmate_response.json()
    print(f'{datetime.datetime.now().time().isoformat()} Poll sugarmate')
    return sm


def time_to_stop():
    stop_running = False
    if msvcrt.kbhit():
        # Read the pressed key
        key = msvcrt.getch()
        print('Would you like to quit? (Y/N)')
        time.sleep(7)
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key in [b'y', b'Y']:
                stop_running = True
                print('Stop running..')
        if not stop_running:
            print('Continues..')
    return stop_running


def sync_loop():
    """
    Runs the sync loop
    """
    # Startup
    print('Sugarmate2Nightscout')
    print(f'Version: {sugarmate2nightscout.VERSION}')
    print()
    print('Press a key to stop program')
    print()
    print('More info see:')
    print(sugarmate2nightscout.GITHUB_URL)
    print()

    cfg = read_cfg()
    headers = {'api-secret': hashlib.sha1(cfg['api_secret'].encode('utf-8')).hexdigest(),
               'Content-Type': 'application/json',
               "Accept": "application/json"}
    ns_url = f"{cfg['nightscout_url']}/api/v1/entries.json"

    last_cgm_time = 0
    keep_running = True
    while keep_running:
        # Read json from sugarmate
        sm = read_sugarmate(cfg)
        while (sm['x'] == last_cgm_time) and keep_running:
            print(f'{datetime.datetime.now().time().isoformat()} Wait for new values')
            time.sleep(cfg['retry_interval'])
            cfg = read_cfg()
            keep_running = not time_to_stop()
            sm = read_sugarmate(cfg)

        if keep_running:
            # Convert to nightscout entry
            entry = {
                'sgv': sm['value'],  # Glucose value in mg/dL
                'date': sm['x'] * 1000,  # Time since 1970-01-01 in milliseconds (epoch*1000)
                'dateString': sm['timestamp'],  # UTC time in ISO 8601 format
                'direction': DIRECTIONS[sm['trend']],  # String describing trend
                'trend': sm['trend'],  # Trend code
                'device': 'sugarmate2ns',  # Device name
                'type': 'sgv'  # Glucose data
            }

            print(
                f"Read time: {datetime.datetime.fromtimestamp(sm['x']).time().isoformat()}, value: {sm['mmol']} mmol/L")
            # Save to nightscout
            r = requests.post(url=ns_url,
                              headers=headers,
                              json=entry)
            if not r.ok:
                print('Something went wrong while saving to Nightscout')
                print(f'Response code {r.status_code}')
                print(f'Message\n{r.text}')
            last_cgm_time = sm['x']

        # wait to next sync
        wait_time = max(cfg['sync_phase'] - (time.time() - last_cgm_time), cfg['retry_interval'])
        print(f'{datetime.datetime.now().time().isoformat()} wait for: {datetime.timedelta(seconds=wait_time)}')
        time.sleep(wait_time)

        # Reread configuration file
        cfg = read_cfg()
        keep_running = not time_to_stop()

    print('Terminate sync loop!')


def get_cfg_filename():
    """
    Return name of configuration file

    The configuration file can be:
    1. Passed by command line
    2. Stored on _home folder_/sugarmate2nightscout.yaml
    3. Same folder as script ./sugarmate2nightscout.yaml
    :return:
    """
    home_cfg_file = os.path.join(HOMEFOLDER, DEFAULT_CFG_FILE)
    local_cfg_file = os.path.join(os.path.dirname(sys.argv[0]), DEFAULT_CFG_FILE)
    if len(sys.argv) >= 2:
        return sys.argv[1]
    elif os.path.isfile(local_cfg_file):
        return local_cfg_file
    elif os.path.isfile(home_cfg_file):
        return home_cfg_file
    else:
        print("Can't find configuration file")
        print('')
        print('Sugarmate2Nightscout expect to find  a configuration file in one of three different places.')
        print('1. Command line parameter')
        print(f'2. In the same folder ({local_cfg_file})')
        print(f'3. In the home directory  ({home_cfg_file})')
        print(
            'More information about the configuration can be found on https://github.com/Josef-A/sugarmate2nightscout')
        print()
        raise NoConfigfile('Could not find any configuration file')


if __name__ == '__main__':
    sync_loop()
