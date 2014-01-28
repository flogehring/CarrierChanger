ChangeCarrierName
=================

Python script for changing the carrier name of the iOS Simulator


In order to write to the system folders it's required to call this script with sudo.
So only use it if you know what you are doing.  
You are responsible for you own system.

Usage Examples: 
---------------

####Changing the carrier name for all languages:

	sudo carrierchange.py -c "My new carrier"

####Changing the carrier name for english and german:

	sudo carrierchange.py -c "My new carrier" -l en de

####Reset all languages to their defaults. These are stored in defaultValues.json

	sudo carrierchange.py -r

####Create defaultsValues.json from your system settings. Note that this overwrites the exisiting one

	sudo carrierchange.py -b



TODO:
-----

- Enable restoring for a given set of languages only
