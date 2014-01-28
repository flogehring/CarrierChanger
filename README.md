CarrierChanger
=================

Python script for changing the carrier name of the iOS Simulator.


In order to write to the system folders it's required to call this script with `sudo`.  
So only use it if you know what you are doing. You are responsible for your own system.

Usage Examples: 
---------------

###Change all the things
Change the carrier name for all languages.

	sudo carrierChange.py -c "My new carrier"

###Picking languages
Changing the carrier name for english and german.

	sudo carrierChange.py -c "My new carrier" -l en de

###Reset 
Reset all languages to their defaults. These are stored in defaultValues.json

	sudo carrierChange.py -r

###Backup
Create defaultsValues.json from your system settings. This can be useful with newer iOS releases.

	sudo carrierChange.py -b



Todo
-----

- Enable restoring for a given set of languages only


Credit
-------
This is all based on a [Stackoverflow answer](http://stackoverflow.com/questions/12580694/how-to-customize-carrier-name-in-ios-6-simulator/14292811#14292811) by [Felix Krause](https://github.com/KrauseFx)
