# Netmiko handling additional prompts
import netmiko
import pprint
"""
# many commands require user prompt to compleate our task etc
# we call this a multi-line command
# this is a problem because we dont get back the command prompt of the device which is what netmiko looks for
"""

# handling prompts
# Solution 1, expect_string
"""
device1 = {
    'host': 'cisco1.lasthop.io',
    'username': 'pyclass',
    'password': 'garfield',
    'device_type': 'cisco_ios',
    'session_log': 'my_session.txt',
}
net_connect = netmiko.ConnectHandler(**device1)
print(net_connect.find_prompt())

command = 'delete flash:/cisco_file.txt'
# the below command will give us a timeout error as it's stuck waiting for you to confirm you want to del the file
net_connect.send_command(command)

# solution 1 to expected prompts:

# to get around the prompt we will use the expect_string input in send_command
# WARNING YOU need to be careful using this,
# expect string is a regular expression pattern certin charaters have special meaning such as [, ], %, etc
# note its best practice to use raw strings, however these strings are still being used as

    # [confirm] is the actual output string we expect to be prompt with and
    #we must know this in advance to set up our send commands properly
    # remember the square brackets have meaning in regular expressions!
        #note this is why we will just use r'confirm' in our expect_string

net_connect.send_command(command, expect_string=r'confirm')
# if the confirm is seen in the output we will then exicute our second send_command with our response
# this second command is how we set up our response to the expect_string
# we use expect_string again as netmiko by default tries to hit an enter to verify the prompt
# nimkio will not be able to deturmine the prompt correctly so we manualy look for the #
# the # shows us we are at the active enable terminal. NOTE this wouldnt work if the terminal was >

net_connect.send_command('y', expect_string=r'#')

# recap
net_connect.send_command(command, expect_string=r'confirm')
# we will now add the strip_prompt=False and strip_command=False to clean up our output
# this way we get a nicer output without the command and prompt echos
net_connect.send_command(command, expect_string=r'#', strip_prompt=False, strip_command=False)
"""
# Solution 2, send_command_timing:
"""
# rather than using send_command with the expect_string option set you can use send_command_timing
# send_command_timing() uses a set amount of time before netmiko determines that the command has been executed
# waits a certen amount of time to as a way to determine if the command is done executing

device1 = {
    'host': 'cisco1.lasthop.io',
    'username': 'pyclass',
    'password': 'garfield',
    'device_type': 'cisco_ios',
    'session_log': 'my_session.txt',
}
net_connect = netmiko.ConnectHandler(**device1)
print(net_connect.find_prompt())

command = 'delete flash:/cisco_file.txt'
output = net_connect.send_command_timing(command, strip_command=False, strip_prompt=False)
output = net_connect.send_command_timing('y', strip_command=False, strip_prompt=False)
print(output)

# this works because after the first command has waited netmiko assumes it has successfully completed,
# and moves to the next command that we set up to send as the response
# after waiting a given amount of time netmiko assumes the second command is complete and assumes we are at the terminal
"""
# using global delay factor, delay factor, and fast_cli
"""

# when screen scraping it is hard to determine when the thing we are doing has completed
# we dont want to scrape the screen if our actions haven't completed
# netmiko uses the delays to get around this problem
    1. global_delay_factor
        -this is an int argument for our ConnectHandler
            ex  'global_delay_factor:' 2
        -is a delay multiplier
    2. delay factor
        -you can set delays as an argument in the .send_command() method
        -this only delays the single command you are sending
            net_connect.send_command("show ip int brief", delay_factor=5)
            net_connect.send_command_timing("show ip int brief", delay_factor=5)
# if both delay factors are set it will choose the larger delay
# delay factors cant be used to speed things up, use fast cli

# to speed things up use the ConnectHandler argument fast_cli=True
    # this essentialy changes the global delay, do not use global delay to speed things up
    # when using this is will always take the fastest delay given
    # the trade off to running faster is less reliability, so use with caution
    # use asynco!

# example code

device1 = {
    'host': 'cisco1.lasthop.io',
    'username': 'pyclass',
    'password': 'garfield',
    'device_type': 'cisco_ios',
    'session_log': 'my_session.txt',
    'global_delay_factor': 2,
}
net_connect = netmiko.ConnectHandler(**device1)
output = net_connect.send_command("sh run", delay_factor=3)

#note the delay will be 3 times the normal time not 2


    
# example dict setup for fast_cli

device1 = {
    'host': 'cisco1.lasthop.io',
    'username': 'pyclass',
    'password': 'password',
    'device_type': 'cisco_ios',
    'fast_cli': True
}

"""
# textFSM
"""
# when screen scraping all we get back is a block a text
# generally we want to get back structured data.  Lists, dictionarys etc
# one way to get structured data is by using regular expressions however this takes time
# textFSM is code that helps you structure your data, don't reinvent the wheel
# textFSM templates found at:
    https://github.com/networktocode/ntc-templates
    templates match to commands for each platform
    template must match the command to work
# by defualt netmiko looks for ntp-templates in your home directory (keep it here!)
# you can also set an environment variable so you can export the NET_TEXTFSM and point to the templates directory
    cat .bashrc | tail -1
    export NET_TEXTFSM=/path/to/ntc-templates/templates/
# use the templates by setting textfsm_template=True in the send_command() and send_command_timing() methods



device1 = {
    'host': 'cisco1.lasthop.io',
    'username': 'pyclass',
    'password': 'garfield',
    'device_type': 'cisco_ios',
    'session_log': 'my_session.txt',
    'global_delay_factor': 2,
}

# to use textFSM make sure it is in the proper location or being pointed to
# set textfsm_template=True in the send_command() and send_command_timing() methods
net_connect = netmiko.ConnectHandler(**device1)
output = net_connect.send_command("sh ip interface brief", delay_factor=3, textfsm_template=True)

# notice we get back structured data!  we a list that contains dictionaries
# using pprint is a nice way to look at the structured data

# remember to disconnect
net_connect.disconnect()
"""
# netmiko configuration changes
"""
# you can send configuration changes two ways:
# 1. From a list or single string, using send_config_set() method
    # the netmiko method send_config_set() is used to make config changes
    # netmiko handles getting into the config mode you want, etc etc
    # you can make multipale config changes by passing send_config_set() a list of all the config commands
# 2. From a file, using the send_config_from_file() method
    # this method takes the string to the filepath as the input and 

# netmiko automatically enters and exits config mode for you

# problems you can run into:
    -sending the wrong command
        -there is no error handling 
    -sending a non config command in send_config
        -once again you will get an error
        -in cisco try to stay away from using do in config.  It works but its not a good habit
    -very large set of commands
        -netmiko can be super super slow this is being worked on

# example code

device1 = {
    'host': 'cisco1.lasthop.io',
    'username': 'pyclass',
    'password': 'garfield',
    'device_type': 'cisco_ios',
    'session_log': 'my_session.txt',
    'global_delay_factor': 2,
}

net_connect = netmiko.ConnectHandler(**device1)
# to change configs used the sent_config_set()
config = ['logging buffered 20000', 'no logging console', 'clock timezone EST -5 0']

# note this sends our list of config commands
output = net_connect.send_config_set(config)
print(output)

net_connect.send_config_from_file(config_file='config_filepath.txt')

# remember to shut down connection
net_connect.disconnect()

"""
# scp with netmiko
"""
# the file_transfer() function is what we use for scp

# for scp to work you need to import both ConnectHandler and file_transfer
    # from netmiko import ConnectHandler, file_transfer

# scp in netmiko uses two channels to work:
    - use an ssh control channel to do certain operations
    - uses a separate ssh scp channel to transfer the file
    - kind of like ftp that has a control channel and a data channel 

#scp automatically:
    - checks to see if you have enough space
    - checks if files exists in given filepaths
    - automatically does a md5 hash check
    - if file in dest_file argument exists it checks the md5 hash of that file to see if it is the same file
        -if the md5 hashes are the same the nothing is done 
        -file_transfer knows/thinks the dest_file is the same so no copy operations are preformed

# to use scp a file you need the following arguments:
    source_file - "filepath of file we are copying"
    dest_file - "filepath where we are putting the copied source file"
    direction - ("get" or "put") the direction of the scp relative to where we are running the command
    file_system - the remote file system (ex "bootflash:")
    
    #optional commands:
    overwrite_file - (True or False)

# create a separate dictionary for the above functions to use as your input arguments, 
# note it needs the ssh_conn argument which is an ConnectHandler object

# problems you can run into:
    - the ssh_conn times out
        - this can happen on large files and other files that take a long time
        - make sure your vty timeout doesn't timeout before the transfer is compleate
    - trying to do a transfer while bouncing though a bastion host
        - the scp ssh control channel wont work
        - in cisco ios you can use inline transfer mode to bounce though the bastion host
        - the inline transfer happens all within one ssh channel,
        - note: inline transfer will do a ttl file transfer and only works with text files
            - you can't send binary files in inline transfer mode
    - transfer_file only works with a limited group of ios platforms, meaning the device_type doesn't support scp
        - this is a small list!
       
# A bastion host is a special-purpose computer on a network specifically designed and configured to withstand attacks. 
# The computer generally hosts a single application, for example a proxy server,
# and all other services are removed or limited to reduce the threat to the computer
    
# example code

device1 = {
    'host': 'cisco1.lasthop.io',
    'username': 'pyclass',
    'password': 'garfield',
    'device_type': 'cisco_ios',
    'session_log': 'my_session.txt',
    'global_delay_factor': 2,
}

scp_dict = {
    'source_file': 'testx.txt',
    'dest_file': 'testx.txt',
    'direction': 'put',
    'file_system': 'bootflash:',
    'overwrite_file': True
}

# we name the connection ssh_conn because that is the name of the argument that file_transfer takes
ssh_conn = netmiko.ConnectHandler(device1**)
# note you need to input the ssh_conn connection as the first input
    # This is the connection object NOT the dictionary we used to set that connection up

# we update our scp_dict dictionary so we can use the dictionary as an argument in file_transfer
scp_dict.update({'ssh_conn': ssh_conn})

# we name our varable transfer_dict rather than output becuase file_transfer returns a dictionary
transfer_dict = netmiko.file_transfer(**scp_dict)
print(transfer_dict)

# notice transfer_dict returns a dictionary with information about our file_transfer
    # file_exist - tells us if the dest_file exists on the remote machine and dose it's md5 hash match source_file
        # (True of False)
    # file_transferred - tells us if the file_transfer actually happened
        # if file_exist=True, and file_transferred=True you know something weird happened
    # file_verified - tells us of md5 hash verification was used in our file_transfer function
        # note md5 hash verification can be turned off as an argument in file_transfer
"""
# using netmiko's save_config() example
""" 
# this method is just like running rm mem in cisto


# example code
device1 = {
    'host': 'cisco1.lasthop.io',
    'username': 'pyclass',
    'password': 'garfield',
    'device_type': 'cisco_ios',
    'session_log': 'my_session.txt',
    'global_delay_factor': 2,
}

net_connect = netmiko.ConnectHandler(**device1)
print(net_connect.find_prompt())

output = net_connect.send_config_from_file('my_config_file.txt')
print(output)

# save the config changes so they remain after a reboot (the equivalent to running wr mem)
# this is supported on a lot of the operating systems in netmiko

save_out = net_connect.save_config()
print(save_out)
"""
# ssh key example
"""
# setup to use a ssh key for a given user inside cisco ios is cumbersome,
# once keys are setup they are bound to the username

# if you use ssh keys ConnectHandler no long requires the argument password but now requires:
    use_keys - must be set to True (set to True defualt is False)
    key_file - filepath string to the ssh key you use to connect to the device with

# note you can use ssh proxies
# https://pynet.twb-tech.com/blog/automation/netmiko-proxy.html?__s=4tlrjds8fu5yh73gu7u4
    -proxies do not work well if you are running windows, mush harder to set up
    # note we now need the key_file and use_keys arguments.
    # The ssh key must also be bound to the username in the device we are connecting to

device1 = {
    'host': 'cisco1.lasthop.io',
    'username': 'pyclass',
    'device_type': 'cisco_ios',
    'session_log': 'my_session.txt',
    'use_keys': True,
    'key_file': 'filepath/to/the/ssh/key',
    'fast_cli': True
}

net_connect = netmiko.ConnectHandler(**device1)
print(net_connect.find_prompt())
output = net_connect.send_command("show ip arp", use_textfsm=True)
pprint(output)
net_connect.disconnect()
"""
# interacting with devices though python outside of script / programs
"""

# example code

device1 = {
    'host': 'cisco1.lasthop.io',
    'username': 'pyclass',
    'password': 'garfield',
    'device_type': 'cisco_ios',

}

net_connect = netmiko.ConnectHandler(**device1)
print(net_connect.find_prompt())

output = net_connect.send_command("show ip arp", use_testfsm=True)
print(output)
#net_connect.disconnect()

# if you dont disconnect you can drop into the interpreter shell after running the python script using ipythons -i
# ipython -i test_dict.py
# you should get a python command prompt after the script runs
# in this command prompt you can now run more commands and interact with the connected device
# though netmiko python methods
dir(net_connect)
help(net_connect.config_mode)
# you usualy dont use the method config_mode() because you use net_connect.send_config_set() in your programs
# manuly enter config mode
net_connect.config_mode()
net_connect.exit_config_mode()
# check if you are in enable mode
net_connect.enable()

#write and read to established channels
    # this is a low level way of sending ssh commands and reading the ssh output

# write_channel works with ssh, telnet and console, channels
    # note you need to add a \n to the end of the command you are sending
net_connect.write_channel("show ip int brief\n")

# read from channel
    #(there needs to be some time between when this is ran and when you run the read command)
output = net_connect.read_channel()

# you can change the device type when you are logged into the terminal server of endpoint device
# this is usually done and manually logging into the device using read_channel() and write_channel()
# more on this can be found under netmiko issues
net_connect.redispatch()
"""

########################## HOMEWORK ############################
# Exercises:
"""
My solutions to the exercises can be found at:

https://github.com/ktbyers/pyplus_course/tree/master/class2/exercises?__s=4tlrjds8fu5yh73gu7u4

"""
# Problem 1
"""
1. Use the extended 'ping' command and Netmiko on the 'cisco4' router. 
This should prompt you for additional information as follows:

cisco4#ping
Protocol [ip]: 
Target IP address: 8.8.8.8
Repeat count [5]: 
Datagram size [100]: 
Timeout in seconds [2]: 
Extended commands [n]: 
Sweep range of sizes [n]: 
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/4 ms

a. Use send_command_timing() to handle the additional prompting from this 'ping' command. 
Specify a target IP address of '8.8.8.8'

b. Use send_command() and the expect_string argument to handle the additional prompting. 
Once again specify a target IP address of '8.8.8.8'.
"""

# Problem 2
"""
2. Create a Netmiko connection to the 'nxos2' device using a global_delay_factor of 2. 
Execute 'show lldp neighbors detail' and print the returned output to standard output. 
Execute 'show lldp neighbors detail' a second time using send_command() with a delay_factor of 8. 
Print the output of this command to standard output. 
Use the Python datetime library to record the execution time of both of these commands. 
Print these execution times to standard output.
"""
#Problem 3
"""
3. On your AWS lab server, look at the ntc-templates index file (at ~/ntc-templates/templates/index). 
Look at some of the commands available for cisco_ios 
(you can use 'cat ~/ntc-templates/templates/index | grep cisco_ios' to see this). 
Also look at some of the abbreviated forms of Cisco IOS commands that are supported in the index file.

Create a script using Netmiko that executes 'show version' 
and 'show lldp neighbors' against the Cisco4 device with use_textfsm=True.

What is the outermost data structure that is returned from 'show lldp neighbors' 
(dictionary, list, string, something else)? 
The Cisco4 device should only have one LLDP entry (the HPE switch that this router connects to). From this LLDP data, 
print out the remote device's interface. In other words, 
print out the port number on the HPE switch that Cisco4 connects into.
"""
# Problem 4
"""
4. Use Netmiko and the send_config_set() method to configure the following on the Cisco3 router.

ip name-server 1.1.1.1
ip name-server 1.0.0.1
ip domain-lookup

Experiment with fast_cli=True to see how long the script takes to execute (with and without this option enabled).

Verify DNS lookups on the router are now working by executing 'ping google.com'. 
Verify from this that you receive a ping response back.
"""

# Problem 5
"""
5. On both the NXOS1 and NXOS2 switches configure five VLANs including VLAN names 
(just pick 5 VLAN numbers between 100 - 999). 
Use Netmiko's send_config_from_file() method to accomplish this. 
Also use Netmiko's save_config() method to save the changes to the startup-config.
"""

# Problem 6
"""
6. Using SSH and netmiko connect to the Cisco4 router. 
In your device definition, specify both an 'secret' and a 'session_log'. Your device definition should look as follows:

password = getpass()
device = {
    "host": "cisco4.lasthop.io",
    "username": "pyclass",
    "password": password,
    "secret": password,
    "device_type": "cisco_ios",
    "session_log": "my_output.txt",
}

Execute the following sequence of events using Netmiko:
a. Print the current prompt using find_prompt()

b. Execute the config_mode() method and print the new prompt using find_prompt()

c. Execute the exit_config_mode() method and print the new prompt using find_prompt()

d. Use the write_channel() method to send the 'disable' command down the SSH channel. 
Note, write_channel is a low level method so it requires that you add a newline to the end of your 'disable' command.

e. time.sleep for two seconds and then use the read_channel() method 
to read the data that is currently available on the SSH channel. Print this to the screen.

f. Execute the enable() method and print your now current prompt using find_prompt(). 
The enable() method will use the 'secret' defined in your device definition. 
This 'secret' is the same as the standard lab password.

g. After you are done executing your script, 
look at the 'my_output.txt' file to see what is included in the session_log.


Notes: both the send_config_set() and send_config_from_file() methods automatically enter and exit config mode; 
consequently, you don't typically need to control this yourself. 
The write_channel() and read_channel() methods can be useful 
if you need to make a custom solution to write/read the SSH channel in some way. 
The session_log can be very helpful for debugging Netmiko issues to see what occurred during the SSH session.

"""