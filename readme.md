# sugarmate2nightscout


Simple script to copy glucose data from Sugarmate to Nightscout

## The original problem with data from Dexcom is solved
The problem were that the Dexcom user name contained other characters than a-z. For instance period.
Read more about that in:
https://github.com/nightscout/cgm-remote-monitor/issues/5608

I wrote some instructions of how to change the Dexcom account. See [here](how_to_fix_en.md) or [here](how_to_fix_sv.md) for a Swedish variant.

Then you do not need to use this script.
This script will probably not be maintained. But I leave it up  here for the documentation of this problem.



## Limitations
This is quick workaround. The code does not have proper handling of errors for example.
Use at your own risk. Nothings guarantied.

The sugarmate API only gives the latest glucose value. That means that it is not possible to backfill with older data. If the transmitter loses connection the gaps won’t be filled later on.

Another limitation for the moment is that the script do not check if the glucose reading for that time already exists in Nightscout. I would like to fix that in a future release. This might have some impact of the quality of the Nightscout data. It might be good to disable the bridge plugin to avoid duplicate of data.


## Background
Nightscout usually fetch glucose data from Dexcom by using Dexcoms share API.
For some user that has not worked since 2020-04-09. Nightscout did not get any new data. But Dexcoms follow app still works.
See https://github.com/nightscout/cgm-remote-monitor/issues/5608 for more information.

Dexcom share API has two methods to get glucose data. One method is intended to be used by the sender app. That's the method Nightscout usually use.
Another method is to act as a follower. It's more complicated as you have to implement some routines to handle invitations. It also has the drawback that it uses one Dexcom follower.
 
This workaround uses the follow method to get glucose data. The Dexcom share API does not have a full public documentation. The best I have seen is https://github.com/nightscout/share2nightscout-bridge/issues/15

Unfortunately there is not enough information to implement routines to handle follower.
But Sugarmate have solved that. They have implemented a routine to act as a follower to Dexcom.


## Setup sugarmate2nightscout

### Prerequisite
You will need a computer with internet connection that will be on for all time.

The script is tested with Python 3.7.4.
It will probably run on most Python 3 versions. I happened to use a module that is only available for windows. (msvcrt). The same functionality can be found in modules for Linux. In a future release I would like to use a more portable approach.

The binaries for Windows have been tested on Windows 10 and Windows 2016.


### Sugarmate

* Set up an account at Sugarmate
* Connect to Dexcom as a follower
* Activate external JSON API 
* Remember the URL to the JSON API

Sugarmate have good instructions for these steps
https://sugarmate.io/

### Install sugarmate2nightscout

I have not made any proper deployment routine for the Python script. You can just checkout the code from github.

For simplicity I have prepared a binary file to be used in Windows.  
That can be downloaded from https://github.com/Josef-A/sugarmate2nightscout/releases

I will described how to install the binary file. But it will be the same if you use the Python code. The difference is that you run the file sync_data.py instead.


* Download the binary file. 
* Place a configuration file in the same folder
* Edit the configuration file with your settings 

Remember that the configuration files stores the API_SECRET for your Nightscout in plain text. It could be an good idea to place the configuration file in a folder with restricted access if several people have acces to the computer.

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
 
### Questions, errors etc.
 Please use the issue tracker on Github:
  https://github.com/Josef-A/sugarmate2nightscout/issues
  
Since I done this code hastily I anticipate some bugs in the near future. Please report them.
Suggestions and contributions is also welcomed.  
  
### Future
The best would be if someone could implement this routine as an extension to the bridge plugin of Nightscout. Then the plugin could use normal retrieve method and have this as a fallback method if the primary method doesn't work. Best would of cause be if Nightscout could handle follower. Then we do not need to go via Sugarmate.

Things I would like to add is for example:

* Check if a glucose reading already exists in Nightscout
* Better error handling
* Another method to start/stop the script. Would also make the script portable to other platforms than Windows.
* Routine that check if normal routine of Nightscout (share2bridge) starts work again.
* Ability to handle more than one Nightscout user
* Otimization of poll timing
* Deploy to PyPi


But I will not put in any time in this if no one needs this features. Please open an issue [at](https://github.com/Josef-A/sugarmate2nightscout/issues) if you would like me to implement some of these features. Also if you have any other needs or suggestions. 



### License
GNU Affero General Public License (AGPL)  