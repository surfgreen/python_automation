import sys
from pprint import pprint


# Python Libraries and PIP
"""
# how to rename a function that you are importing
from re import search as my_search

my_search() # this is the new name for re

# when using pip look how active the project is
# pip install <library name>
# can use pip to install older packages

# command to see all the packages installed
# pip list

# gives the current state of all the packages
# pip freeze

# pip freeze is useful for recreating an environment
# this is super useful when recreating virtual environments!

# pip freeze > requirements.txt

# you can now use requirements.txt with pip -r to install the packages given to you from the freeze
# this recreates the same pip environment

# pip install -r ./requirements.txt
"""
# sys.path and PYTHONPATH
"""
# this command shows us the paths python searches for packages
# when you import a library these are the folders python looks for it in
pprint(sys.path)

# if you made your own python package name with an existing library name there will be a conflict
# for example if we made a python file called re.py in our working directory it would import that
# rather than the re library that comes with python


# its best practice to reuse your code you've made rather than constantly copying it
# you do this my making modules
# modules are python files that contain your code that you can import into new projects
# remember to not use a name that's already in use
# place the python file (module) in one of the folders shown with the sys.path command

# __file__
# to see what sys.path a varible was loading from use __file__

# import my_module
# my_module.__file__

# modifying the sys.path
# in linux you can modify your sys.path in a BASH terminal

# shows you your PYTHONPATH - this is where you should keep the code (modules) you want to reuse later
# env | grep PYTHON

# note this will not return anything because you have set the PYTHONPATH using the export command first

# sets your PYTHONPATH to what you want it to be
# export PYTHONPATH=~/PyCharm/python-libs

# note if you run
"""

# reusing code from previously made programs using __name__
"""
# your code should have the following structure:
    # importable code at the top
        # things we might use later
            # functions
            # constants
            # classes
            # etc
    # executable code at the bottom
        # where you put your functions together at the end to make your code actualy do something

# program functions that can be imported later (our building block)

# def main(): # note main is importable!

# if __name__ == "__main__":
    # main()
    # code that is executed
    # code under here is not imported
    # when you imported into other programs


# __name__
    # __name__ is automaticly set to "__main__" when executing

    #import test_module
    # __name__ is set to the module name if it is imorted

# this is how we separate importable code from executable code!
"""
# TextFSM
"""
# TextFSM was originally created by google
# FSM sands for finite state machine 
# TextFSM helps us phrasing with string outputs 
# to use this you must know how to use regular expressions

# what is a finite-state machine
# note we use $$ to get a $ in textFSM
''''
 finite-state machine (FSM) or finite-state automaton (FSA, plural: automata), 
 finite automaton, or simply a state machine, is a mathematical model of computation. 
 It is an abstract machine that can be in exactly one of a finite number of states at any given time. 
 The FSM can change from one state to another in response to some inputs; 
 the change from one state to another is called a transition
''''


# example template for TextFSM file:

TextFSM File

# Define your fields to extract 
Value VAR_NAME (regex_pattern) 
Value VAR_NAME (regex_pattern)
Value VAR_NAME (regex_pattern)

# Start of the FSM
Start
# notice the below ^Device.*ID is a regular expression
#
    ^Device.*ID -> LLDP
    
LLDP
    ^${VAR_NAME}.* -> Record
    
# Implicit EOF and Record
#EOF



# example TextFSM file with comments:

TextFSM File

# Define your fields to extract 
Value VAR_NAME (regex_pattern) 
Value VAR_NAME (regex_pattern)
Value VAR_NAME (regex_pattern)

# Start of the FSM
Start
# notice the below ^Device.*ID is a regular expression
# if the ^Device.*ID pattern is detected it transistions into the LLDP state
    ^Device.*ID -> LLDP
    
LLDP
# ^${VAR_NAME}.* is how we defined the LLDP state
# This expresstion is defined to Record an entry
    ^${VAR_NAME}.* -> Record
    
# Implicit EOF and Record
#EOF (end of file)
"""
# creating a TextFSM template
"""
When making a template its useful to copy the output you get from the command
This way you can see it when you are writing your expressions

Value INTERFACE (\S+)

Start
    ^${INTERFACE}\s+ -> Record

EOF

Notice the out out when we use this template we will make it better moving forword


Value INTERFACE (\S+)
Value IP-ADDR (\S+)

Start
    ^Interface.*Protocol\s*$$ -> ShowIPIntBrief  #filters out our first interface output then moves us to the new state
    
ShowIPIntBrief
    ^${INTERFACE}\s+${IP_ADDR}\s+ -> Record

EOF


# how to run testFSM in the terminal
python textfsm.py <templateName.template> <string_output.txt>

# continuing the example:

Value INTERFACE (\S+)
Value IP-ADDR (\S+)
Value LINE_STATUS (up|down)
Value LINE_PROTOCOL (up|down)

Start
    ^Interface.*Protocol\s*$$ -> ShowIPIntBrief  
    
ShowIPIntBrief
    ^${INTERFACE}\s+${IP_ADDR}.*${LINE_STATUS}\s+${LINE_PROTOCOL}\s*$$ -> Record

EOF


# make sure you make the template so it works with lots of different outputs
# and you have a way to fix problems without breaking what you had working

# example 2:
    # example template using the sh version command

Value MODEL (\S+)  
Value MEMORY (\d+K)
Value SERIAL_NUMBER (\S+)
Value CONFIG_REGISTER (0x\d+)



Start
    ^cisco ${MODEL}\s+.*processor with ${MEMORY}/\d+K bytes of memory
    ^Processor board ID ${SERIAL_NUMBER}
    ^Configuration register is ${CONFIG_REGISTER} -> Record

# example 3:
    # using the command sh ip bgp
    # notice not all the fields show up in output sometimes
    # this is why we use textFSM!  the state machine helps us  

# this code doesnt get all the data from the columns.
# to get all the data we use a Filldown shown incorperated into the template code below this code

Value VALID_BEST ([*>]+)
Value PREFIX (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}) # regex for IPv4 address
Value NEXT_HOP (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})

Start
    ^\s+Network.*Path\s*$$  -> ShowIPBgp

ShowIPBgp
    ^ ${VALID_BEST}\s+${PREFIX}\s+${NEXT_HOP} -> Record

EOF

# code with Filldown
# Filldown tells our state machine that if it hits our variable save it for later use
# now when our regular expresstion goes on and doesn't find a value in the row below
# it will use the last saved value for the value of the blank space
# we also need to add a regular expression to the ShowIPBgp state 
# to account for a time it doesnt find our PREFIX expression


Value VALID_BEST ([*>]+)
Value Filldown PREFIX (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}) # regex for IPv4 address
Value NEXT_HOP (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})

Start
    ^\s+Network.*Path\s*$$  -> ShowIPBgp

ShowIPBgp
    ^ ${VALID_BEST}\s+${PREFIX}\s+${NEXT_HOP} -> Record
    ^ ${VALID_BEST}\s+${NEXT_HOP} -> Record

EOF


# There is also a Fillup (fills in varibles from the bottom up) , Required , etc

# python example of how to use textFSM (not in netmiko)

import textfsm

# name of template you want to use, could be one you made
template_file = "show_ip_int_brief.template"
template = open(template_filepath)

#text file you are filtering 
with open("show_ip_int_bried.txt") as f:
    raw_text_data = f.read()
    
# the argument 'template' is a file handle and 'raw_text_data' is a string

# parse your template using the textfsm class passing in your template file
re_table = textfsm.TextFSM(template)
# we use the method .ParseText()
data = re_table.ParseText(raw_text_data)

# remember to close the file you opened
template.close()

# after you get the returned data you can then change the data structure
# this is something you must do

"""



#Exercises:
"""
My solutions to the exercises can be found at:
https://github.com/ktbyers/pyplus_course/tree/master/class4/exercises?__s=4tlrjds8fu5yh73gu7u4

1. Using the following 'show interface status' output:

Port      Name  Status       Vlan  Duplex Speed Type
Gi0/1/0         notconnect   1     auto   auto  10/100/1000BaseTX
Gi0/1/1         notconnect   1     auto   auto  10/100/1000BaseTX
Gi0/1/2         notconnect   1     auto   auto  10/100/1000BaseTX
Gi0/1/3         notconnect   1     auto   auto  10/100/1000BaseTX


Create a TextFSM template that extracts only the 'Port' column (i.e. the interface name). 
The output of the FSM table should look as follows:

$ textfsm.py ex1_show_int_status.tpl ex1_show_int_status.txt
...
FSM Table:
['PORT_NAME']
['Gi0/1/0']
['Gi0/1/1']
['Gi0/1/2']
['Gi0/1/3']



2. Expand the TextFSM template created in exercise1 such that you extract the 
Port, Status, Vlan, Duplex, Speed, and Type columns. 
For the purposes of this exercise you can ignore the 'Name' column and assume it will always be empty. 
The output of the FSM table should look similar to the following:

$ textfsm.py ex2_show_int_status.tpl ex2_show_int_status.txt
...
FSM Table:
['PORT_NAME', 'STATUS', 'VLAN', 'DUPLEX', 'SPEED', 'PORT_TYPE']
['Gi0/1/0','notconnect','1','auto','auto','10/100/1000BaseTX']
['Gi0/1/1','notconnect','1','auto','auto','10/100/1000BaseTX']
['Gi0/1/2','notconnect','1','auto','auto','10/100/1000BaseTX']
['Gi0/1/3','notconnect','1','auto','auto','10/100/1000BaseTX']



3. Using the 'show interface Ethernet2/1' output from nxos1 (see link below), 
extract the interface name, line status, admin state, MAC address, MTU, duplex, and speed using TextFSM.

https://github.com/ktbyers/pyplus_course/blob/master/class4/exercises/ex3_nxos_show_interface_ethernet_2_1.txt


4. Use TextFSM to parse the 'show arp' output from a Juniper SRX (see link below). 
Extract the following fields into tabular data: MAC Address, Address, Name, Interface.

https://github.com/ktbyers/pyplus_course/blob/master/class4/exercises/ex4_junos_show_arp.txt


5. Parse the 'show lldp neighbors' output from nxos1 (see link below). 
From this output use TextFSM to extract the Device ID, Local Intf, Capability, and Port ID.

https://github.com/ktbyers/pyplus_course/blob/master/class4/exercises/ex5_nxos_show_lldp_neighbors.txt


6. Parse the following 'show ip bgp summary' output (see link below). 
From this output, extract the following fields: Neighbor, Remote AS, Up_Down, and State_PrefixRcvd. 
Also include the Local AS and the BGP Router ID in each row of the tabular output (hint: use filldown for this). 
Note, in order to simplify this problem only worry about the data shown in the output (in other words, 
don't worry about all possible values that could be present in the output).

Second hint: remember there is an implicit 'EOF -> Record' at the end of the template (by default).

https://github.com/ktbyers/pyplus_course/blob/master/class4/exercises/ex6_show_ip_bgp_summary.txt


7. Using your TextFSM template and the 'show interface status' data from exercise2, 
create a Python program that uses TextFSM to parse this data. In this Python program, 
read the show interface status data from a file and process it using the TextFSM template. From this parsed-output, 
create a list of dictionaries. The program output should look as follows:

$ python ex7_show_int_status.py

[{'DUPLEX': 'auto',
  'PORT_NAME': 'Gi0/1/0',
  'PORT_TYPE': '10/100/1000BaseTX',
  'SPEED': 'auto',
  'STATUS': 'notconnect',
  'VLAN': '1'},
 {'DUPLEX': 'auto',
  'PORT_NAME': 'Gi0/1/1',
  'PORT_TYPE': '10/100/1000BaseTX',
  'SPEED': 'auto',
  'STATUS': 'notconnect',
  'VLAN': '1'},
 {'DUPLEX': 'auto',
  'PORT_NAME': 'Gi0/1/2',
  'PORT_TYPE': '10/100/1000BaseTX',
  'SPEED': 'auto',
  'STATUS': 'notconnect',
  'VLAN': '1'},
 {'DUPLEX': 'auto',
  'PORT_NAME': 'Gi0/1/3',
  'PORT_TYPE': '10/100/1000BaseTX',
  'SPEED': 'auto',
  'STATUS': 'notconnect',
  'VLAN': '1'}]
"""