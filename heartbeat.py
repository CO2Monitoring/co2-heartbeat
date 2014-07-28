#!/usr/bin/python

import json
import hashlib
from hmac import new as hmac
import urllib2
import datetime
import os
import stat
from netifaces import interfaces, ifaddresses, AF_INET

domain = "http://co2.example.com"
deviceid_file = "/home/co2/etc/deviceid"
devicekey_file = "/home/co2/etc/devicekey"

# Reading device ID
try:
        f = open(deviceid_file,'r')
        device_id = f.readline().strip()
        f.close()
except IOError:
        exit("Can't open "+deviceid_file)

# Checking secret key file permissions
st = os.stat(devicekey_file)
if bool(st.st_mode & stat.S_IRGRP):
        print "[ERROR] File containing device secret key ("+devicekey_file+") is group readable. Run chmod 600 /etc/co2/devicekey",
        exit()

if bool(st.st_mode & stat.S_IROTH):
        print "[ERROR] File containing device secret key ("+devicekey_file+") is readable by anyone. Run chmod 600 /etc/co2/devicekey",
        exit()


# Reading device secret key
try:
        f = open(devicekey_file,'r')
        device_key = f.readline().strip()
        f.close()
except IOError:
        exit("[ERROR] Can't open file containing device secret key ("+devicekey_file+")")

# Fetching devices and ip addresses
ifaces = []
for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'disconnected'}] )]
    if ifaceName!='lo':
        iface = {}
        iface["name"] = ifaceName
        iface["ip"] = ', '.join(addresses)
        ifaces.append(iface)

# Producing JSON
#dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) else None
data = json.dumps({'interfaces': ifaces, 'timestamp': datetime.datetime.utcnow().isoformat(), 'device_id': device_id, 'uri': '/heartbeats', 'loadavg': os.getloadavg()})

# Signing JSON
signature = hmac(device_key, data, hashlib.sha256).digest().encode('base64').strip()

# Sending POST request to /heartbeat

# DEBUG
#handler=urllib2.HTTPHandler(debuglevel=1)
#opener = urllib2.build_opener(handler)
#urllib2.install_opener(opener)

req = urllib2.Request(domain+"/heartbeats")
req.add_header('Authorization','HMAC '+signature)
req.add_header('Accept','application/json')
req.add_header('Content-Type','application/json')
try:
    res = urllib2.urlopen(req,data)
except urllib2.HTTPError:
        # TODO ??
        exit("HTTP error")
