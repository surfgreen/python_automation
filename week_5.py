from jinja2 import Template
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

# templating
"""
# Jinja 2 is the best templating library for python
    # automating emails
    # config files
    # etc

# templates work the following way:
#Variables -> Templates -> Generated Files
"""
# jinja2 flow control structure
"""

# flow control is used for (for loops, conditionals, etc)
# example set up of jinja2 flow control
    # double curly braces can generally contain expressions {{ variable }}
        # typically the varible being rendered

# This is code embedded in a text file 
# notice the syntax has indicates the code blocks start and end {{% endif %}

# example flow control structure

Variables: {{ vlan1 }}

Confitionals:

{% if var == 'value' %}
string of output text
{% elif var == 'other value' %}
next string of output text
{% else %}
the else clause
{% endif %}

For Loops:

{% for item in some_list %}
string of output {{ item }}
{% endfor %}

{# This is a comment in Jinja2 #}
"""
# jinja2 Data Structures
"""

# example data structue

List: {{ some_list[0] }}

#Loop over lists using a for-loop

Dictionary: 

{{ a_dict["key"] }}
# you can also use:
{{ a_dict.key }}

# Loop over dictionary using the below code:

{% for key in my_dict %}
{{ key }}
{% endfor %}

{% for k, v in my_dict.items() %}
Some test {{ k }} and {{ v }}
{% endfor %}


"""
# jinja2 Variables
# example python code using jinja2 variables
# example 1
"""
#from jinja2 import Template

text1 = '''
this is some template
that has multiple lines
of text in it
it is a string
'''

bgp_config = '''
router bgb 42
 bgp router-id 10.22.88.20
 bgp log-neighbor-changes
 neighbor 10.220.88.38 remote-as 44
'''

# make a jinja2 object
j2_template = Template(text1)
# render the jinja2 object
output = j2_template.render()
# notice we didn't use variables so we just got back out text1 string
print(output)
"""
# example 2
"""
bgp_config = '''
router bgb {{ bgp_as }}
 bgp router-id 10.22.88.20
 bgp log-neighbor-changes
 neighbor 10.220.88.38 remote-as 44
'''

example_expr = '''
some text with expressions {{ 13 + 3}}
other expressions {{ 13 * 7 }}
hello
'''

# make a jinja2 object
my_template = bgp_config
# my_template = example_expr

j2_template = Template(my_template)
# notice we now set our template variable in the .render() method
output = j2_template.render(bgp_as=22)
# notice we didn't use variables so we just got back out text1 string
print(output)

# notice the exprections in the template are evaluated and the out put is printed
j2_example_expr = Template(example_expr)
output_2 = j2_example_expr.render()
print(output_2)
"""
# example 3
"""
bgp_config = '''
router bgb {{ bgp_as }}
 bgp router-id {{ router_id }}
 bgp log-neighbor-changes
 neighbor {{ peer1 }} remote-as 44
'''
j2_template = Template(bgp_config)
# notice we now set our template variable in the .render() method
output = j2_template.render(bgp_as=22, router_id="1.1.1.1", peer1="10.20.30.1")
# notice we didn't use variables so we just got back out text1 string
print(output)
"""
# example 4
"""
# passing in variables to the .renter() method can be done with dictionarys
# use this for your variables!!!

bgp_config = '''
router bgb {{ bgp_as }}
 bgp router-id {{ router_id }}
 bgp log-neighbor-changes
 neighbor {{ peer1 }} remote-as 44
'''
my_vars = {
    'bgp_as': '22',
    'router_id': '1.1.1.1',
    'peer1': '10.20.30.1'
}

j2_template = Template(bgp_config)
# notice we now set our template variable in the .render() method
output = j2_template.render(**my_vars)
# notice we didn't use variables so we just got back out text1 string
print(output)
"""
# jinja2 Environment
# example 5
"""
# jinja2 files have the .j2 extension
# open the .j2 template when you want to use the template
# you then pass your varibales to the varibles defined in the template

filename = 'bgp_filepath.j2'
with open(filename) as f:
    my_template = f.read()

template_vars = {
    'bgp_as': 22,
    'router_id': '1.1.1.1',
    'peer1': '10.10.10.1'
}

j2_template = Template(my_template)
output = j2_template.render(**template_vars)

"""
# example 6
"""
# problem with last example
    # problems occur when you have undefined variables, your code is missing variables, etc
    # your program cant find the template because its stored in a different location
    # your template references other templates

# solution:
    # use a jinja2 enviorment
# from jinja2 import FileSystemLoader, StrictUndefined
# from jinja2.environment import Environment

# enforce failing when undefined variables are used
# error: jinja2.exceptions.UndefinedError:
env = Environment(undefined=StrictUndefined)
#set dictorys we will look for the template file in
#env.loader = FileSystemLoader('.')
#env.loader = FileSystemLoader('./templates/')
# use a list to look in multipul directors
env.loader = FileSystemLoader(['./templates/', '.'])

bgp_vars = {
    'bgp_as': 22,
    'router_id': '1.1.1.1',
    'peer1': '10.10.10.1'
}

# name of template file
template_file = 'bgp_config.j2'
# use env.get_template() method to find a template defined by the template_file
template = env.get_template(template_file)
output = template.render(**bgp_vars)
"""
# jinja2 Whitespace
"""
# these are defined in our flow control
# dealing with newlines and spaces in our templates when they are strings
# when we render and have variables they are rendered with extra spaces
# we get extra newlines and spaces
# example template with whitespace
'''
interface GigabitEthernet0/0/0
 {% if primary_ip %}
 ip address 10.22.0.88.22 255.255.255.0
 {% endif %}
 negotiation auto
'''

# we can get rid of whitespace by doing the following:
# '%-'  - this strips out leading whitespace and newline charter at the end of the line
# '-%'  - this strips out the newline, and the next lines whitespace before the variable
# notice the - strips out whitespace before and after it

# example of the most common pattern of striping whitespace in the template
'''
interface GigabitEthernet0/0/0
 {%- if primary_ip -%}
 ip address 10.22.0.88.22 255.255.255.0
 {%- endif %}
 negotiation auto
'''
"""
# standard python jinja2 loader code:
"""
env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader(['./templates/', '.'])

template_vars = {}

# the template
template_file = "template1.j2"
template = env.get_template(template_file)
output = template.render(**template_vars)
print(output)
"""
# jinja2 conditionals
"""
# from jinja2 import FileSystemLoader, StrictUndefined
# from jinja2.environment import Environment


env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader(['./templates/', '.'])

# notice the template has a if primary_ip statement
# primary_ip is set to a boolean value,  if statements require boolean inputs 
my_vars = {
    'primary_ip': True
}

'''
# the template
interface GigabitEthernet0/0/0
{% if primary_ip %}
ip address 10.22.0.88.22 255.255.255.0
{% endif %}
negotiation auto
'''

template_file = 'intf_config1.j2'
# use env.get_template() method to find a template defined by the template_file
template = env.get_template(template_file)
output = template.render(**my_vars)

# be careful using to many programing constructs in your flow control
# keep it as simple as you can
# push your complexity to your python or program itself

# example template using elif:

interface GigabitEthernet0/1/0
  {%- if mode == "access" %}
  switchport access vlan 400
  switchport mode access
  {%- elif mode == "trunk" %}
  switchport trunk natice vlan 1
  switchport trunk allowed vlan 1-400
  switchport mode trunk
  {%- else %}
  shutdown
  description <== DISABLED ==>
  {%- endif %}

"""
# nested conditional template example
"""
# defined asks if a variable exists in the inputs.
    # would return false if the varible doesnt exist
 {%- if bgp_peer1 is defined %}
 neighbor {{ peer_ip }}
  address-family ipv4 unicast
   {%- if bgb_policy is defined %}
   route-policy ALLOW in
   route-policy ALLOW out
   {%- endif %}
 {%- endif %}
"""
# jinja2 Loops
"""
Loops are great for setting up interfaces

example template code:
{%- for port_number in range(24) %}
interface fastEthernet0/1/{{ port_number }}
switchport access vlan 400
switchport mode access
!
{%- endfor %}


#remember you can make a quick list of number in python by doing
#list(range(1, 24)) # etc etc
#list(range(24))

# its nice to have the list construction and interface names handled in python
# many ports such as uplink ports are different than the ports on the rest of the device

example template code:
{%- for intf in inif_list %}
interface {{ intf }}
switchport access vlan 400
switchport mode access
!
{%- endfor %}

from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader(['./templates/', '.'])

# we handle making the interface list in python rather than the template
base_intf = 'GigabitEthernet0/1/'
intf_list = []

for intf_number in range(24):
    # f string does the same thing as the .format() method
    intf_name = f"{base_intf}{intf_number}"
    int_list.append(intf_name)
 
int_vars = {
    'intf_list': intf_list,
    }

# name of template file
template_file = 'intf_config2.j2'
# use env.get_template() method to find a template defined by the template_file
template = env.get_template(template_file)
output = template.render(**intf_vars)
print(output)

"""
# nested for loops in templates
"""
# could want this due to number of blades in device
# example nested loop template code

{%- for slot in range(1,4) %}
 {%- for port_number in range(1,25) %}
interface GigabitEthernet0/{{ slot }}/{{ port_number }}
 {%- endfor %}
{%- endfor %}


# example nested loop with conditional
# only prints out port 10s 
{%- for slot in range(1,4) %}
 {%- if port_number == 10 %}
interface GigabitEthernet0/{{ slot }}/{{ port_number }}
 {%- endif %}
{%- endfor %}

"""
# jinja2 lists
"""
# example of setting up list in data structure
List: {{ some_list[0] }}

#Loop over lists using a for-loop

# example using a list in the template

text in template
more text

{# First element: #}
{{ int_list[0] }}

{# Last element: #}
{{ int_list[-1] }}

{# length of list:  in this line length is a jinja2 filter #}}
{{ int_list | length }}

{# Entire list: #}
{{ int_list }}

"""
# jinja2 Dictionaries
"""
# example of dictionary set up in data structure

Dictionary: 

{{ a_dict["key"] }}
{# you can also use a_dict.key instead of ["key"]#}

Loops:

{% for key in my_dict %}
{{ key }}
{% endfor %}

{% for k, v in my_dict.items() %}
Some test {{ k }} and {{ v }}
{% endfor %}


# example of putting the jinja2 code all together

Some text
Hello World

ARP Interface:
{{ arp_entry["interface"] }}

MAC --> IP
{{ arp_entry['mac' }} --> {{ arp_entry["ip"] }}

For loop in dict:
{%- for k in arp_entry %}
    {{ k }}
{%- endfor %}


For loop in dict (using dict items):
{%- for k, v in arp_entry.items() %}
 {{ k }} --> {{ v }}
{%- endfor %}


# example python code

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader(['./templates/', '.'])

arp_entry = {
    'interface': "mgmt0",
    "ip": "10.0.0.72",
    "mac": "2C:C2:60:36:32:21",
    "age": 140.0
    }


# notice we use arp_entry as varible
template_vars = {
    arp_entry": arp_entry,
}

# the template
template_file = "template1.j2"
template = env.get_template(template_file)
output = template.render(**template_vars)
print(output)

"""
# creating variables and filters in jinja2 templates
"""
# example of creating variables
    # notice the key word set

{%- set var1 = 'Cisco' %}
{%- set var1 = 'Arista' %}
{%- set var1 = 'Juniper' %}

{{ var1 }}
{{ var2 }}
{{ var3 }}


# example of creating a filter
    # use the pipe | to pipe varibles through filters

{%- set var1 = 'Cisco' %}
{%- set var1 = 'Arista' %}
{%- set var1 = 'Juniper' %}
{%- set my_list = ['cisco', 'arista', 'juniper']

{{ var1 | capitalize }}


{{ var2 | capitalize | center(80) }}

{{ var3 }}

# this tells your code to set var4 to "Some Default Value" if it isn't yet defined
{{ var4 | default("Some Default Value")  }}

{{ my_list  }}

"""
# includes in jinja2
"""
# including code is useful for using global variables in templates 
# example template that includes another template:

some text
{% include 'other_template.j2' %}
more text
{% include 'another_template.j2' %}

# dynamically include a template notice the template isn't a string
    # we can pass in a filename using a variable used in our setup dictionary
    # this is called when calling the .render() method 
some text
{% include template_var %}
footer text

"""
# jinja2 misc:
"""
Jinja2 has functions and they are called macros
Jinja2 templates can also have, template inheritance 
Jinja2 has built in filters
Jinja2 is much more than these notes
"""

# Exercises:
"""
My solutions to the exercises can be found at:
https://github.com/ktbyers/pyplus_course/tree/master/class5/exercises?__s=4tlrjds8fu5yh73gu7u4



1. Create a Python program that uses Jinja2 to generate the below BGP configuration.
Your template should be directly embedded inside of your program as a string and
should use for the following variables: local_as, peer1_ip, peer1_as, peer2_ip, peer2_as.

router bgp 10
  neighbor 10.1.20.2 remote-as 20
    update-source loopback99
    ebgp-multihop 2
    address-family ipv4 unicast
  neighbor 10.1.30.2 remote-as 30
    address-family ipv4 unicast


2a. Use Python and Jinja2 to generate the below NX-OS interface configuration.
You should use an external template file and a Jinja2 environment to accomplish this. T
he interface, ip_address, and netmask should all be variables in the Jinja2 template.


nxos1
interface Ethernet1/1
  ip address 10.1.100.1/24

nxos2
interface Ethernet1/1
  ip address 10.1.100.2/24



2b. Expand your Jinja2 template such that both the following interface and BGP configurations
are generated for nxos1 and nxos2. The interface name, IP address, netmask, local_as, and peer_ip
should all be variables in the template. This is iBGP so the remote_as will be the same as the local_as.

nxos1

interface Ethernet1/1
  ip address 10.1.100.1/24

router bgp 22
  neighbor 10.1.100.2 remote-as 22
    address-family ipv4 unicast


nxos2

interface Ethernet1/1
  ip address 10.1.100.2/24

router bgp 22
  neighbor 10.1.100.1 remote-as 22
    address-family ipv4 unicast



2c. Use Netmiko to push the configurations generated in
exercise 2b to the nxos1 device and to the nxos2 device, respectively.
Verify you are able to ping between the devices and also verify that the BGP session reaches the established state.
Note, you might need to use an alternate interface besides
Ethernet 1/1 (you can use either Ethernet 1/1, 1/2, 1/3, or 1/4).
Additionally, you might need to use a different IP network (to avoid conflicts with other students).
Your autonomous system should remain 22, however.

For this exercise you should store your Netmiko connection dictionaries in an external file named my_devices.py and
should import nxos1, and nxos2 from that external file.
Make sure that you use getpass() to enter the password in for these devices
(as opposed to storing the definitions in the file).

Note, this exercise gets a bit complicated when it is all said and done (templating, pushing configuration to devices,
verifying the changes were successful).


3. Generate the following configuration output from an external Jinja2 template:

vrf definition blue
 rd 100:1
 !
 address-family ipv4
  route-target export 100:1
  route-target import 100:1
 exit-address-family
 !
 address-family ipv6
  route-target export 100:1
  route-target import 100:1
 exit-address-family


Both the IPv4 and the IPv6 address families should be controlled by Jinja2 conditionals
(in other words, the entire 'address-family ipv4' section and
the entire 'address-family ipv6' sections can be dropped from the generated output
depending on the value of two variables that you pass into your template--for example,
the 'ipv4_enabled' and the 'ipv6_enabled' variables).
Additionally, both the vrf_name and the rd_number should be variables in the template.
Make sure that you control the whitespace in your output such that the configuration looks visually correct.


4. Expand on exercise3 except use a for-loop to configure five VRFs.
Each VRF should have a unique name and a unique route distinguisher.
Each VRF should once again have the IPv4 and the IPv6 address families
controlled by a conditional-variable passed into the template.

Note, you will want to pass in a list or dictionary of VRFs that you loop over in your Jinja2 template.


5. Start with the full running-config from cisco3.lasthop.io as a base template (for example 'cisco3_config.j2').
Modify this base template such that you use Jinja2 include statements to pull in sub-templates for the NTP servers,
the AAA configuration, and for the clock settings.

Your base template should have the following items (in the proper locations):

{% include 'aaa.j2' %}

{% include 'clock.j2' %}

{% include 'ntp.j2' %}


The child templates being pulled in should contain the NTP configuration, the AAA configuration,
and the clock configuration. The two NTP servers, the timezone, timezone_offset,
and timezone_dst (daylight savings timezone name) should be variables in these child templates.

The output from this should be the full configuration which is basically identical
to the current running configuration on cisco3.lasthop.io.

"""