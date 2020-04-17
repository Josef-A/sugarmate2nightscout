# sugarmate2nightscout


Simple script to copy glucose data from Sugarmate to Nightscout

## Limitations
This is quick workaround. The code does not have proper handling of errors for example.
Use at your own risk. Nothings guarantied.

The sugarmate API only gives the latest glucose value. That means that it is not possible to backfill with older data. If the transmitter loses connection the gaps wont be filled later on.

Another limitation for the moment is that the script do not check if the glucose reading for that time already exists in Nightscout. I would like to fix that in a future release. This might have some impact of the quality of the Nightscout data. It might be good to disable the bridge plugin to avoid duplicate of data.


## Background
Nightscout usually fetch glucose data from Dexcom by using Dexcoms share API.
For some user that has not worked since 2020-04-09. Nightscout did not get any new data. But Dexcoms follow app still works.
See https://github.com/nightscout/cgm-remote-monitor/issues/5608 for more information.

Dexcom share API has two methods of get glucose data. One method is intended to be used by the sender app. That's the method Nightscout usually use.
Another method is to act as a follower. It's more complicated as you have to implement some routines to handle invitations. It also has the drawback that it uses one Dexcom follower.
 
This workaround uses the follow method to get glucose data. The Dexcom share API does not have a full public documentation. The best I have seen is https://github.com/nightscout/share2nightscout-bridge/issues/15

Unfortunately there is not enough information to implement routines to handle follower.
But sugarmate have solved that. They have implemented a routine to act as a follower to Dexcom.


## Setup sugarmate2nightscout

### Sugarmate

* Set up an account at sugarmate
* Connect to Dexcom as a follower
* Activate external JSON API 
* Remember the URL to the JSON API

Sugarmate have good instructions for these steps
https://sugarmate.io/

### Install sugarmate2nightscout

I have not made any proper deployment routine for the Python script. You can just checkout the code from github.

For simplicity I have prepared an binary file to be used in Windows.  
That can be downloaded from https://github.com/Josef-A/sugarmate2nightscout/releases

I will described how to install the binary file. But it will be the same if you use the Python code. The difference is that you run the file sync_data.py instead.


* Download the binary file. 
* Place a configuration file in the same folder
* Edit the configuration file with your settings 


#### Configuration file
A sample of a configuration file can be found 
[here](./configuration_template/sugarmate2nightscout.yaml)

You have to edit three fields in the configuration file

* sugarmate_url (The url to sugarmate JSON API)
* nightscout_url
* api_secret

The configuration file uses yaml-syntax

The script looks after the configuration file in three places


1. Passed as parameter in the command line
2. Same folder as script ./sugarmate2nightscout.yaml
3. Stored on _home folder_/sugarmate2nightscout.yaml

### Run sugarmate2nightscout
Just run the binary file.
It will open up a console. To stop running just press a key while the console is active. Then wait (maybe 5 min) for a question if you would like to quit.
This isn't a nice solution of terminate the program, but I hadn't time for a proper solution.
It's also safe to terminate the script while it's waiting to poll next time.

To work as intended you have to run it on a computer that's stays on and connected to internet. Make sure you turn off any sleep mode.
 
### Questions, errors etc
 Please use the issue tracker on Github:
  https://github.com/Josef-A/sugarmate2nightscout/issues
  
Since I done this code hastily I anticipate some bugs in the near future. Please report them.
Suggestions and contributions is also welcomed.  
  
### Future
The best would be if someone could implement this routine as a extension to the bridge plugin of Nightscout. Then the plugin could use normal retreive method and have this as a fallback method if the primary method doesn't work. Best would of cause be if Nightscout could handle follower. Then we do not need to go via sugarmate.


### License
GNU Affero General Public License (AGPL)  