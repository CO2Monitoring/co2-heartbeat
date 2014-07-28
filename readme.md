# Heartbeat script for Rapsberry Pi CO2 sensor

## Installation
	$ sudo apt-get install python-pip python-dev
	$ sudo pip install netifaces
	$ sudo su - co2
	$ mkdir /home/co2/etc && chmod 700 /home/co2/etc
	$ sudo echo "YOUR_DEVICE_ID" >> /home/co2/etc/deviceid
	$ sudo echo "YOUR_DEVICE_KEY" >> /home/co2/etc/devicekey
	$ sudo chmod 600 /home/co2/etc/devicekey

	
Edit crontab to run the script regularly

	$ sudo chmod 700 /home/co2/heartbeat/heartbeat.py
	$ sudo crontab -e

Add the following line in the editor
	
	* * * * * /home/co2/heartbeat/heartbeat.py

# Copyright #

Copyright (c) 2014, [Marat Vyshegorodtsev][2] & [Graham Weldon][3]

# License #

Licensed under the [MIT License][1].

[1]: http://www.opensource.org/licenses/mit-license.php
[2]: http://maratto.blogspot.com
[3]: http://grahamweldon.com