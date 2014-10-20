CarrierChanger
=================

Python script for changing the carrier name of the iOS Simulator.


In order to write to the system folders it's required to call this script with `sudo`.  
So only use it if you know what you are doing. You are responsible for your own system.

![](example.png)

Usage Examples: 
---------------

###Change all the things
Change the carrier name for all languages.

	sudo python carrierChanger.py -c "My new carrier"

###Picking languages
Changing the carrier name for english and german.

	sudo python carrierChanger.py -c "My new carrier" -l en de

###Reset 
Reset all languages to their defaults. These are stored in defaultValues.json

	sudo python carrierChanger.py -r

###Backup
Create defaultsValues.json from your system settings. This can be useful with newer iOS releases.

	sudo python carrierChanger.py -b


###Change the time
This changes the system time of your Mac to **09:41** and restarts the simulator. 

	sudo python charrierChanger.py -tc

###Reset the time
This resets the system time of your Mac by syncing with Apple's servers and restarts the simulator.

	sudo python charrierChanger.py -ts

Todo
-----

- Enable restoring for a given set of languages only
- Dynamically get the latest simulator version so it's not hard-coded

Credit
-------
This is all based on a [Stackoverflow answer](http://stackoverflow.com/questions/12580694/how-to-customize-carrier-name-in-ios-6-simulator/14292811#14292811) by [Felix Krause](https://github.com/KrauseFx)
