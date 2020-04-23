# Probable solution to the problem with data from Dexcom share

## What is the problem
It seems that Dexcom share somewhere in its systems is not capable of using the username other than ordinary letters.

By changing the username, this has been solved for everyone who has tried so far.
If that doesn't work for you, please report it at https://github.com/nightscout/cgm-remote-monitor/issues/5608 or if you can comment on any Facebook post that linked to this site.

## Disclaimer 
I made these instructions from a Swedish context. It might be different in your country.
I also have no idea how it works if you use Dexcom connected with a pump. 

## Change username
Unfortunately, it is not possible to change the username of a Dexcom account. You have to create a whole new account.

### Create new account
Go to https://www.dexcom.com and look for where to create account.
Follow the instructions to create a new account. You can only associate an email address with one Dexcom account.
Make sure to use another email for the new account. The alternative is to delete the old account. But do **not** do that. It may be good to be able to go back and retrieve historical data.
Make sure the new username contains only letters. It is best to stick to a-z. We know that the period sign creates problems. But we do not know what other signs there are problems with.

### Reinstall Dexcom Transmitter app
This is how it works under Android. I guess it is similar for IPhone.
When you install the Dexcom G6 app, it is linked to a Dexcom account. Unfortunately, there is no way to switch accounts. What you have to do is simply uninstall the app and reinstall it.
In principle, it is the same procedure as changing a telephone. 
Of course, this time you should log in with the new account.
* Write down the current Transmitter ID. You can find the ID if you look in settings in the G6 app.
* Uninstall the G6 app
* Reinstall the G6 app
* Log in with new account
* Follow the instructions in the app.
* Do not select sensor code. The sensor code is already saved on your old transmitter.
* Enter the sender's ID and wait for pairing
* Answer yes to the question "have you inserted sensor"

Then you have to re-invite any followers you want.


### Nightscout
* Log in to Heroku https://www.heroku.com/
* Find the project with your Nightscout
* Click _Settings_
* Click < Reveal Config Vars >
* Change _BRIDGE_USER_NAME_ and _BRIDGE_PASSWORD_ to match the new account
* Make sure _bridge_ is included in _ENABLE_

When you change these variables, Heroku restarts Nightscout. So now everything should work

### Diasend
You must switch so that Diasend retrieves data from the new account.
Diasend receives data from Dexcom with quite a delay. In order to lose as little data as possible, it is best to wait until all data from the old account has come to Diasend. It can take several days.
After that, it's just to:
* Log in to Diasend https://diasend.com/
* Go to "Connect apps"
* Press _Disconnect_ under Dexcom G5 / G6
* Then press _Connect_
* Log in with your new Dexcom account

## Is it working?
Please let us know if this helped. Either in response to Facebook on the post that linked here or at https://github.com/nightscout/cgm-remote-monitor/issues/5608

Especially important that you write something if it not works for you.

   / Josef