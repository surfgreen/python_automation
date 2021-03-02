# Screen Scraping vs APIs
"""
#Screen scrapings
-SSH and telnet we use screen scraping
-Is unaware of the commands and data that is being sent
-Time it takes the command to complete
-Get back strings and have to parse the strings ourselves
-built for humans so sometimes run into colors, ascii escape codes, and other artifacts that are hard to process
-etc

#APIs
-Better awareness of the command being executed
-Not full of ascii charters, and other artifacts
-typically returns structured data
-can still have version issues

"""
# Arista eAPI
"""
-Uses https
-Uses JSON
-Is not a RESTFUL API
-REST APIs:
    -the url changes when you access different resources
    -Uses http GET when retrieving information
    -Uses http POST when creating things 
    -Uses http PUT when you are modifying things 
"""
# eAPI Device Configutation:
"""
management api http-commands
    protocol https
    no shutdown
"""
# JSON-RPC Request Structure
"""
{
    "jsonrpc": "2.0",
    "method": "runCmds",
    "params": {
        "version": 1,
        "cmds": [
            "show version"
        ],
        "format": "json"
    },
    "id": "1" # this the unique ID so we know what requests go to what responses
}
"""
# JSON-RPC Response
"""
{
    "id": "1",  # out matching unique ID
    "jsonrpc": "2.0",
    "result": [
        {
            "architecture": "i386",
            "bootupTimestamp": 15436048.0,
            "hardwareRevision": "",
            "internalBuildId": "68f3ae78-65cb-4ed3-8675-0ff2219bf11",
            "internalVersion": "4.20.10M-10040268.42010M",
            "isIntlVersion": false,
            "memFree": 3282936,
            "memTotal": 4011056,
            "modelName": "vEOS",
            "serialNumber": "",
            "systemMacAddress": "52:54:ab:da:54:95",
            "uptime": 8596.91,
            "version": "4.20.10M"
        }
    ]
}
"""

# Making a eAIP using low level request python code (not the API library)
# example 1
"""
# note not all CLI commands work as API commands!
# need bonus class to get the REST API videos

# review ipdb!
import requests # 3rd party library but is pythons fundamental way of interfacing with APIs
import json
from pprint import pprint
from getpass import getpass

from urllib3.exceptions import InsecureRequestWarning
import ipdb # debugger for ipython

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

if __name__ == "__main__":

    ipdb.set_trace() # use "n" then hit enter in the promp    print()t to step through the code
    http_headers = {"Content-Type": "application/json-rpc;"}
    host = "arista8.lasthop.io"
    port = 443
    username = "pyclass"
    password = getpass()

    # this is the structure of the url
    url = f"https://{host}:{port}/command-api"

    # json payload string in python
    json_payload = {
    "jsonrpc": "2.0",
    "method": "runCmds",
    "params": {
        "version": 1,
        "cmds": [
            "show version"
        ],
        "format": "json"
    },
    "id": "1" # this the unique ID so we know what requests go to what responses
}
    # convert python json string to json
    json_data = json.dumps(json_payload)
    # get data length
    http_headers["Content-length"] = str(len(json_data))

    response = requests.post(
        url,
        headers=http_headers,
        auth=(username,password),
        data=json_data,
        verify=False,
    )

    response = response.json()
    pprint(response)
"""
# code for sending config constructs
# example 2
"""
# note it is almost identical but the commands ("cmd") we send are set up diffrently

if __name__ == "__main__":

    ipdb.set_trace() # use "n" then hit enter in the promp    print()t to step through the code
    http_headers = {"Content-Type": "application/json-rpc;"}
    host = "arista8.lasthop.io"
    port = 443
    username = "pyclass"
    password = getpass()

    # this is the structure of the url
    url = f"https://{host}:{port}/command-api"

    # note: this code is diffrent because we are sending configs
    cmds = [
        "disable",
        {"cmd": "enable", "input": ""}, # input is our enable secret which in this case is Null so ""
        # notice we need to send the command configure terminal to enter the config mode
        "configure terminal",
        "vlan 255",
        "name green"
    ]

    # json payload string in python
    json_payload = {
    "jsonrpc": "2.0",
    "method": "runCmds",
    "params": {
        "version": 1,
        "cmds": cmds, # we set this to our list of commands we defined above
        "format": "json"
    },
    "id": "1" # this the unique ID so we know what requests go to what responses
}
    # convert python json string to json
    json_data = json.dumps(json_payload)
    # get data length
    http_headers["Content-length"] = str(len(json_data))

    response = requests.post(
        url,
        headers=http_headers,
        auth=(username,password),
        data=json_data,
        verify=False,
    )

    response = response.json()
    pprint(response)
# notice we get back [{}, {}, {}, {}, {}]
# the {} tells us that our command executed successfully 
"""

# Example, using pyeapi (library built by Arista for Aristas API)
"""
# pyeapi is a python library created by Arista
# In general you want to always check to see if there is a library created for the API you are working with
    # try to avoid getting into the low level mechanics of how to interface with the API


import pyeapi
from getpass import getpass
import ipdb

# there are other ways to use this.  This is just one example

# set your debugger
ipdb.set_trace()

# creates a EapiConnection object
connection = pyeapi.client.connect(
    transport="https",
    host="arista8.lasthop.io",
    username="pyclass",
    password=getpass(),
    port="443"
)

enable = getpass("Enable: ")
# this creates a NodeEapi Object EapiConnection object
device = pyeapi.client.Node(connection=connection, enablepwd=enable)

# using the NodeEapi object we can now use methods to get the information about the device
# ex:
print(device.version())
# you can change how the data is retrieved and what config you want
print(device.get_config(config='startup_config', as_string=True))


# the ! is how you can call a command inside the ipdb debugger
!device.get_version_number()

# you can use configuration files in your connections
"""
# Creating connections using pyeapi and .eapi.conf
"""
# example making NodeEapi objects with .eapi.conf file
# you must create the .eapi.conf file yourself
# remember to keep it updated.  Easy to make mistakes when porting code etc

[connection:arista8]
host: asista8.lasthop.io
username: pyclass
password: 88newclass
transport: https

[connection:arista7]
host: asista7.lasthop.io
username: pyclass
password: 88newclass
transport: https


# second example using default, note we no longer need to enter the defualt information for each device

[connection:arista8]
host: asista8.lasthop.io

[connection:arista7]
host: asista7.lasthop.io
username: pyclass

[DEFAULT]
username: pyclass
password: 88newclass
transport: https


# Using the EAPI we can now use that conf file for our connections

import pyeapi

# This creates our NodeEapi Object like in the above example
# arista8 and arista7 are defined in our .eapi.conf file
device1 = pyeapi.connect_to("arista8")
device2 = pyeapi.connect_to("arista7")

# example of getting the device data
print(device1.model())
"""
# Example, using pyeapi to run show commands
"""
import pyeapi
from getpass import getpass
import ipdb

# there are other ways to use this.  This is just one example

# set your debugger
ipdb.set_trace()

# creates a EapiConnection object
connection = pyeapi.client.connect(
    transport="https",
    host="arista8.lasthop.io",
    username="pyclass",
    password=getpass(),
    port="443"
)

enable_pass = getpass("Enable: ")
# this creates a NodeEapi Object EapiConnection object
device = pyeapi.client.Node(connection=connection, enablepwd=enable_pass)
# .enable() is the method that you use to execute show commands makes sure you are in enable mode
# not a good name for what it does
output = device.enable("show version")
print(output)

# use can send a list of commands
output = device.enable(["show ip arp, show version"])
print(output)

# remember in ipython you can drop into your python terminal after the script has run by using -i
# ipython -i example_program.py
# this leaves us with out current context so you can still interact with the objects etc
"""
# Using Eapi to make configuration changes
"""
import pyeapi
from getpass import getpass
import ipdb

# there are other ways to use this.  This is just one example

# set your debugger
ipdb.set_trace()

# creates a EapiConnection object
connection = pyeapi.client.connect(
    transport="https",
    host="arista8.lasthop.io",
    username="pyclass",
    password=getpass(),
    port="443"
)
cfg = [
    "vlan 225",
    "name green",
    "vlan 226",
    "name red",
]

enable = getpass("Enable: ")
# this creates a NodeEapi Object EapiConnection object
device = pyeapi.client.Node(connection=connection, enablepwd=enable)
# send our list of commands given in cfg to the .config() NODE method
output = device.config(cfg)
print(output)

# using the .run_commands() method is the real command that is wrapped 
# by the .config() method and .enable() methods
"""
# using the .api() method
"""
# you can use the .api() method to get into subsystems

import pyeapi
from getpass import getpass
import ipdb

# there are other ways to use this.  This is just one example

# set your debugger
ipdb.set_trace()

# creates a EapiConnection object
connection = pyeapi.client.connect(
    transport="https",
    host="arista8.lasthop.io",
    username="pyclass",
    password=getpass(),
    port="443"
)

enable_pass = getpass("Enable: ")
# this creates a NodeEapi Object EapiConnection object
device = pyeapi.client.Node(connection=connection, enablepwd=enable_pass)

# use the .api() method to see the subsystem vlans, could be any subsystem
vlan_cfg = device.api("vlans")
# notice we get a vlan api object back
print(vlan_cfg)
# gets back our vlan 1
vlan_cfg.get(1)
# create a vlan and name it using .create() and .set_name()
vlan_cfg.create(800)
vlan_cfg.set_name(800, "blue vlan")
"""



#Exercises:
"""
My solutions to the exercises can be found at:

https://github.com/ktbyers/pyplus_course/tree/master/class6/exercises


1. Using the pyeapi library, connect to arista3.lasthop.io and execute 'show ip arp'. From this ARP table data, print out a mapping of all of the IP addresses and their corresponding MAC addresses.

2a. Define an Arista device in an external YAML file (use arista4.lasthop.io for the device). In your YAML file, make sure the key names exactly match the names required for use with pyeapi and the connect() method. In other words, you should be able to execute 'connect(**device_dict)' where device_dict was retrieved from your YAML file. Do not store the lab password in this YAML file, instead set the password using getpass() in your Python program. Using this Arista device information stored in a YAML file, repeat the 'show ip arp' retrieval using pyeapi. Once again, from this ARP table data, print out a mapping of all of the IP addresses and their corresponding MAC addresses.

2b. Create a Python module named 'my_funcs.py'. In this file create two functions: function1 should read the YAML file you created in exercise 2a and return the corresponding data structure; function2 should handle the output printing of the ARP entries (in other words, create a separate function that handles all printing to standard out of the 'show ip arp' data). Create a new Python program based on exercise2a except the YAML file loading and the output printing is accomplished using the functions defined in my_funcs.py.

3. Using your external YAML file and your function located in my_funcs.py, use pyeapi to connect to arista4.lasthop.io and retrieve "show ip route". From this routing table data, extract all of the static and connected routes from the default VRF. Print these routes to the screen and indicate whether the route is a connected route or a static route. In the case of a static route, print the next hop address.

4. Note, this exercise might be fairly challenging. Construct a new YAML file that contains the four Arista switches. This YAML file should contain all of the connection information need to create a pyeapi connection using the connect method. Using this inventory information and pyeapi, create a Python script that configures the following on the four Arista switches: 

interface {{ intf_name }}
   ip address {{ intf_ip }}/{{ intf_mask }}

The {{ intf_name }} should be a Loopback interface between 1 and 99 (for example Loopback99).

The {{ intf_ip }} should be an address from the 172.31.X.X address space. The {{ intf_mask }} should be either a /24 or a /30.

Each Arista switch should have a unique loopback number, and a unique interface IP address.

You should use Jinja2 templating to generate the configuration for each Arista switch.

The data for {{ intf_name }} and for {{ intf_ip }} should be stored in your YAML file and should be associated with each individual Arista device. For example, here is what 'arista4' might look like in the YAML file:

​arista4:
  transport: https
  host: arista4.lasthop.io
  username: pyclass
  port: 443
  data:
    intf_name: Loopback99
    intf_ip: 172.31.1.13
    intf_mask: 30


Use pyeapi to push this configuration to the four Arista switches. Use pyeapi and "show ip interface brief" to display the IP address table after the configuration changes have been made.

"""
