# Complex Data Structures - nested lists that contain lists, dicts that contain dicts, etc etc
import re

"""
step 1: look at to see what type the data structure is (list or dict)
step 2: look at the length of the data structure
step 3: slowly drill down into the nested data to figure out how it is setup
    -its useful to use variables to name the different layers
step 4:  once you understand the data structure write a function to process the data for you


# example of loop that gives us key value varables in for loop though dictionary
test_dict = {'key1': 1, 'key2': 2}
for key, value in test_dict.items():
    print(key)
    print(value)

# converting a data structure to another format:
    # use loops with key value pairs to work with data and build new structures
# example of data structure changes
test_dict = {'key1': 1, 'key2': 2}
test_list = []
for key, value in test_dict.items():
    test_list.append({key: value})
print(test_list)
"""
# Serialization
"""
Serialization - converting things in our program to bytes that can be sent across the wire or be writen to a file
Serialization needed to send data from one device to another, must be platform independent

Examples of Serialization are JSON and YMAL

JSON 
    Is good for computer to computer communications.  
    Is commonly used in web application APIs
    Good for networking devices APIs
    Not good if humans have to write JSON, is picky and very condensed
YAML
    Easy to read and write in its expanded form
    Uses indentation
Serialization - converting things in our program to bytes that can be sent across the wire or be writen to a file
Serialization needed to send data from one device to another, must be platform independent

"""
# YAML
"""
YAML uses indents in its structure
Can be used in compressed or uncompressed
YAML is a super set of JSON and JSON should be able to be understood by YAML parsers

list notation:
---
-first_element
-second_element

dict notation:
---
key1: value1
key2: value2


nested dict example:
---
router1:
  device_type: cisco_iso
  ip_addr: 1.1.1.1
  username: admin
  password: pass123

other types:
---
- some string
- "another string"
# the following is a null value
- null
# booleans
- True
- False
- true
- false
- on
- off
- yes
- no
# strings
- "yes" # needed to keep the string yest from 
- |
  This is a multiline string in YMAL.
  It can have more than one line
  You do this with the pipe |
- >
  This gives us strings with new lines

# notice the lack of indentation!  the list itself is the value to the key somelist
somelist:
- 0
- 1
- 2

"""
# JSON
"""
JSON example

import json

# JSON will not let you put a comma at the end of the last element!
# this wouldn't work: [1,2,3,]  same for dicts

my_data = {
            'key1': 'value1',
            'key2': 'value2' 
            }
some_list = list(range(10))
my_data[some_list] = some_list

filename = "output_file.json"
with open(filename, 'wt') as f:
    # use json.dump() to write to files
    # json.dump(<data>, <file_we_write_to>) 
    json.dump(my_data, f, indent=4) #indent helps you look at the json a lot easier

# use json.dumps() writes the data out as a string

# load JSON to python example
filename = input("Input filename: )
with open(filename) as f:
    data = json.load(f)
"""
# CiscoConfParse
"""
CiscoConfParse - is a  python library that helps us work with configs!
    -turns our config files into a tree structure making it a lot  easier to work with
    
-Works in cisco and cisco like devices
    - this library helps you deal with the interfaces inside cisco config files!
    - gives us the children of the global commands (commands for interfaces)

-Very useful when you are dealing with interfaces that have multiple levels of depth
-Saves us from having to 

example:

from ciscoconfparse import CiscoConfParse

# make a CiscoConfParse object out of our file
cisco_obj = CiscoConfParse("config_file")

# to pass in config information from a string
    # must first convert your config string into a list
    # use the string method .splitlines()
    
my_config = '''
interface f0/1
duplex auto
speed auto
description port shut down
shut
'''

my_obj = CiscoConfParse(my_config.splitlines())

# use this to see what methods CiscoConfParse has
    # notice the find objects methods
    # in general we will mostly use find object methods to help us find structures we care about
print(dir(my_obj))

# use help to see how to use various methods the CiscoConfParse class has 
print(help(my_obj.find_objects))

# notice this method takes in a regular expression 
    # remember to use raw strings when working with regular expressions

# this finds all the interfaces and returns a list of the interfaces
interface = my_obj.find_objects(r"^interface")

# we can now use the children method on the interface object we just created to view the interface configurations
interface[0].children()

# loop over interface commands 
for child in interface[0].children:
    # notice we use the .text method on the child object
    print(child.text)

##########################################
# example that finds interfaces with ip addresses 

from ciscoconfparse import CiscoConfParse

# remember most of the time we load from a file
config_obj = CiscoConfParse("filepath")

# or load from a string converted to a list with new lines
    # This is useful when using netmiko to connect to devices and running show run
config_obj = CiscoConfParse(config_string.splitlines())

# look for any interface with an IP using the .find_objects_w_child method
    # note the parentspec argument and the childspec argument
    # notice the below finds no ip address
cisco_obj.find_objects_w_child(parentspec=r"^interface", childspec=r"ip address)

# finds only the interfaces with ip addresses using the space to filter the no ip address commands out
cisco_obj.find_objects_w_child(parentspec=r"^interface", childspec=r"^\s+ip address)

# gives us a list of cisco objects that are the parent objects that we found using our filter
match = cisco_obj.find_objects_w_child(parentspec=r"^interface", childspec=r"^\s+ip address")

# look at the children of first cisco interface object we found with an IP
match[0].children


example:

config_obj = CiscoConfParse("config_filepath")
parent = config_obj.find_objects(r"^line con 0")

# only finds and returns one IOSCfgLine object so we can get rid of the list and just work with the object
parent = parent[0]

# see if the object is a parent
parent.is_parent

# make a list of IOSCfgLine objects that are objects of the parents children
children = parent.children

a_child = children[1]

# find if the child is a parent or child
a_child.is_parent
a_child.is_child

# return the parent object to the a_child object
parent = a_child.parent

# does the child have siblings 
# (objects that are also children to the same parent) same level in the tree higerarcky*
a_child.siblings

# find all objects without children using .find_objets_wo_child
without_child = cisco_obj.find_objects_wo_child(parentspec=r"^interface", childspec=r"no ipaddress")

match = cisco_obj.find_objects(r"crypto map CRYPTO")
# only has one crypto map so we can change variable match to the object itself instead of the list that contains the obj
match = match[0]
crypto_kids = match.children

# you can search for exprestions in the parents children using the .re_search_children() method
crypto_kid = match.re_search_children(r"set pfs ")

"""


#Exercises:
"""
My solutions to the exercises can be found at:

Class3 Reference Solutions


1. Using the below ARP data, create a five element list. Each list element should be a dictionary 
with the following keys: "mac_addr", "ip_addr", "interface". 
At the end of this process, you should have five dictionaries contained inside a single list.

Protocol  Address      Age  Hardware Addr   Type  Interface
Internet  10.220.88.1   67  0062.ec29.70fe  ARPA  Gi0/0/0
Internet  10.220.88.20  29  c89c.1dea.0eb6  ARPA  Gi0/0/0
Internet  10.220.88.22   -  a093.5141.b780  ARPA  Gi0/0/0
Internet  10.220.88.37 104  0001.00ff.0001  ARPA  Gi0/0/0
Internet  10.220.88.38 161  0002.00ff.0001  ARPA  Gi0/0/0
"""
#
#Regular Expression Special Characters
'''
.       Any Single character
+       One or more times
*       Zero or more times
^       Beginning of line
$       End of line
\w      alphanumeric letters and digits
\W      non-alphanumeric charaters such as punctuation
\s      Whitespace character class
\d      Digit character class
\S      Non-whitespace character class
[]      Construct your own character class
()      Parenthesis to save things
'''

arp_data = '''
Protocol  Address      Age  Hardware Addr   Type  Interface
Internet  10.220.88.1   67  0062.ec29.70fe  ARPA  Gi0/0/0
Internet  10.220.88.20  29  c89c.1dea.0eb6  ARPA  Gi0/0/0
Internet  10.220.88.22   -  a093.5141.b780  ARPA  Gi0/0/0
Internet  10.220.88.37 104  0001.00ff.0001  ARPA  Gi0/0/0
Internet  10.220.88.38 161  0002.00ff.0001  ARPA  Gi0/0/0
'''
arp_data = arp_data.strip()
arp_list = arp_data.splitlines()
print(arp_list)
desired_list = []
keys = arp_list[0].split()
arp_dict = {}
for line in arp_list:
    values = line.split()
    arp_dict.update({keys[e]: values[e] for e in range(len(values))})
    desired_list.append(arp_dict)
print(desired_list)



"""
2a. Create a list where each of the list elements is a dictionary representing one of the network devices in the lab. Do this for at least four of the lab devices. The dictionary should have keys corresponding to the device_name, host (i.e. FQDN), username, and password. Use a fictional username/password to avoid checking the lab password into GitHub.

2b. Write the data structure you created in part 2a out to a YAML file. Use expanded YAML format. How could you re-use this YAML file later when creating Netmiko connections to devices?


3. NAPALM using nxos_ssh has the following data structure in one of its unit tests (the below data is in JSON format).

{
    "Ethernet2/1": {
        "ipv4": {
            "1.1.1.1": {
                "prefix_length": 24
            }
        }
    },
    "Ethernet2/2": {
        "ipv4": {
            "2.2.2.2": {
                "prefix_length": 27
            },
            "3.3.3.3": {
                "prefix_length": 25
            }
        }
    },
    "Ethernet2/3": {
        "ipv4": {
            "4.4.4.4": {
                "prefix_length": 16
            }
        },
        "ipv6": {
            "fe80::2ec2:60ff:fe4f:feb2": {
                "prefix_length": 64
            },
            "2001:db8::1": {
                "prefix_length": 10
            }
        }
    },
    "Ethernet2/4": {
        "ipv6": {
            "fe80::2ec2:60ff:fe4f:feb2": {
                "prefix_length": 64
            },
            "2001:11:2233::a1": {
                "prefix_length": 24
            },
            "2001:cc11:22bb:0:2ec2:60ff:fe4f:feb2": {
                "prefix_length": 64
            }
        }
    }
}

Read this JSON data in from a file.

From this data structure extract all of the IPv4 and IPv6 addresses that are used on this NXOS device. From this data create two lists: 'ipv4_list' and 'ipv6_list'. The 'ipv4_list' should be a list of all of the IPv4 addresses including prefixes; the 'ipv6_list' should be a list of all of the IPv6 addresses including prefixes.


4. You have the following JSON ARP data from an Arista switch:

{
    "dynamicEntries": 2,
    "ipV4Neighbors": [
        {
            "hwAddress": "dc38.e111.97cf",
            "address": "172.17.17.1",
            "interface": "Ethernet45",
            "age": 0
        },
        {
            "hwAddress": "90e2.ba5c.25fd",
            "address": "172.17.16.1",
            "interface": "Ethernet36",
            "age": 0
        }
    ],
    "notLearnedEntries": 0,
    "totalEntries": 2,
    "staticEntries": 0
}


From a file, read this JSON data into your Python program. Process this ARP data and return a dictionary where the dictionary keys are the IP addresses and the dictionary values are the MAC addresses. Print this dictionary to standard output.


5. In your lab environment, there is a file located at ~/.netmiko.yml. This file contains all of the devices used in the lab. Create a Python program that processes this YAML file and then uses Netmiko to connect to the Cisco3 router. Print out the router prompt from this device.

Note, the device dictionaries in the .netmiko.yml file use key-value pairs designed to work directly with Netmiko. The .netmiko.yml also contains group definitions for: cisco, arista, juniper, and nxos groups. These group definitions are lists of devices. Once again, don't check the .netmiko.yml into GitHub.


6. Use Netmiko to retrieve 'show run' from the Cisco4 device. Feed this configuration into CiscoConfParse.

Use CiscoConfParse to find all of the interfaces on Cisco4 that have an IP address. Print out the interface name and IP address for each interface. Your solution should work if there is more than one IP address configured on Cisco4. For example, if you configure a loopback interface on Cisco4 with an IP address, then your solution should continue to work. The output from this program should look similar to the following:

$ python confparse_ex6.py

Interface Line: interface GigabitEthernet0/0/0
IP Address Line:  ip address 10.220.88.23 255.255.255.0



7. You have the following BGP configuration from a Cisco IOS-XR router:

router bgp 44
 bgp router-id 10.220.88.38
 address-family ipv4 unicast
 !
 neighbor 10.220.88.20
  remote-as 42
  description pynet-rtr1
  address-family ipv4 unicast
   route-policy ALLOW in
   route-policy ALLOW out
  !
 !
 neighbor 10.220.88.32
  remote-as 43
  address-family ipv4 unicast
   route-policy ALLOW in
   route-policy ALLOW out


From this BGP configuration, retrieve all of BGP peer IP addresses and their corresponding remote-as. Return a list of tuples. The tuples should be (neighbor_ip, remote_as). Print your data-structure to standard output.

Your output should look similar to the following. Use ciscoconfparse to accomplish this.

BGP Peers:
[('10.220.88.20', '42'), ('10.220.88.32', '43')]
"""