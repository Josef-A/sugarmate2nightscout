"""
License:
GNU Affero General Public License (AGPLv3)

Author:
Josef Andersson April 2020

Github:

"""

import datetime
import hashlib
import os
import sys
import time

import yaml
import requests

from pathlib import Path

# # Get the base directory
# if getattr(sys, 'frozen', None):  # keyword 'frozen' is for setting basedir while in onefile mode in pyinstaller
#     basedir = sys._MEIPASS
# else:
#     basedir = os.path.dirname(__file__)
#     basedir = os.path.normpath(basedir)
#
# # Locate the SSL certificate for requests
# os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(basedir, 'cacert.pem')

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


def read_cfg():
    cfg_filename = get_cfg_filename()
    with open(cfg_filename, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    return cfg


def read_sugarmate(cfg):
    # Read json from sugarmate
    sugarmate_response = requests.get(url=cfg['sugarmate_url'])
    sm = sugarmate_response.json()
    print(f'sugarmate check time: {datetime.datetime.now().isoformat()}')
    return sm


def sync_loop():
    """
    Runs the sync loop
    """

    cfg = read_cfg()
    headers = {'api-secret': hashlib.sha1(cfg['api_secret'].encode('utf-8')).hexdigest(),
               'Content-Type': 'application/json',
               "Accept": "application/json"}
    ns_url = f"{cfg['nightscout_url']}/api/v1/entries.json"
    print(cfg)
    last_cgm_time = 0
    while cfg['enabled']:
        # Read json from sugarmate
        sm = read_sugarmate(cfg)
        while (sm['x'] == last_cgm_time) and cfg['enabled']:
            print('retry')
            time.sleep(cfg['retry_interval'])
            cfg = read_cfg()
            sm = read_sugarmate(cfg)

        if cfg['enabled']:
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

            # print(entry)
            print(f"Time: {datetime.datetime.fromtimestamp(sm['x']).time().isoformat()}, value: {sm['mmol']}")
            # Save to nightscout
            print(f'save to NS time: {datetime.datetime.now().isoformat()}')
            r = requests.post(url=ns_url,
                              headers=headers,
                              json=entry)
            print(r)
            print(r.reason)
            # print(r.text)
            last_cgm_time = sm['x']

        # wait to next sync
        wait_time = max(cfg['sync_phase'] - (time.time() - last_cgm_time), cfg['retry_interval'])
        print(f'time to sleep: {datetime.datetime.now().isoformat()}')
        print(f'wait time: {datetime.timedelta(seconds=wait_time)}')
        time.sleep(wait_time)
        print('Wake up')
        print(f'wake up time: {datetime.datetime.now().isoformat()}')
        # Reread configuration file
        cfg = read_cfg()
        # cfg['enabled'] = False

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
        raise Exception('Miss configuration file')


if __name__ == '__main__':
    sync_loop()
