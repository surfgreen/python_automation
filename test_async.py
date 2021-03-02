import asyncio
from netmiko import ConnectHandler
import getpass
import ipdb

"""
device_dict = {
'cisco3': {
    # 'comment': 'Cisco IOS-XE',
    'host': 'cisco3.lasthop.io',
    # 'snmp_port': 161,
    # 'ssh_port': 22,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'cisco_xe'
},

'cisco': {
    # 'comment': 'Cisco IOS-XE',
    'host': 'cisco4.lasthop.io',
    # 'snmp_port': 161,
    # 'ssh_port': 22,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'cisco_xe'
},

'arista1': {
    # 'comment': 'Arista_vEOS_switch',
    'host': 'arista1.lasthop.io',
    # 'ssh_port': 22,
    # 'eapi_port': 443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'arista_eos'
},

'arista2': {
    # 'comment': 'Arista_vEOS_switch',
    'host': 'arista2.lasthop.io',
    # 'ssh_port': 22,
    # 'eapi_port': 443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'arista_eos'
},

'arista3': {
    # 'comment': 'Arista_vEOS_switch',
    'host': 'arista3.lasthop.io',
    # 'ssh_port': 22,
    # 'eapi_port': 443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'arista_eos'
},

'arista4': {
    # 'comment': 'Arista_vEOS_switch',
    'host': 'arista4.lasthop.io',
    # 'ssh_port': 22,
    # 'eapi_port': 443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'arista_eos'
},

'srx2': {
    # 'comment': 'Juniper_SRX',
    'host': 'srx2.lasthop.io',
    # 'ssh_port': 22,
    # 'netconf_port': 830,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'juniper'
},

'nxos1': {
    # 'comment': 'NX-OSv Switch',
    'host': 'nxos1.lasthop.io',
    # 'ssh_port': 22,
    # 'nxapi_port': 8443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'cisco_nxos'
},

'nxos2': {
    # 'comment': 'NX-OSv Switch',
    'host': 'nxos2.lasthop.io',
    # 'ssh_port': 22,
    # 'nxapi_port': 8443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'cisco_nxos'
}
}
"""
device_dict = {
'cisco3': {
    # 'comment': 'Cisco IOS-XE',
    'host': 'cisco3.lasthop.io',
    # 'snmp_port': 161,
    # 'ssh_port': 22,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'cisco_xe'
},

'cisco': {
    # 'comment': 'Cisco IOS-XE',
    'host': 'cisco4.lasthop.io',
    # 'snmp_port': 161,
    # 'ssh_port': 22,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'cisco_xe'
}
}

exec_send_args = {'command_string': "show run",
                  'expect_string': None,
                  'delay_factor': 1,
                  'max_loops': 500,
                  'auto_find_prompt': True,
                  'strip_prompt': True,
                  'strip_command': True,
                  'normalize': True,
                  'use_textfsm': False,
                  'textfsm_template': None,
                  'use_ttp': False,
                  'ttp_template': None,
                  'use_genie': False,
                  'cmd_verify': True
                  }


# connection dictionary argument setup functions
def binary_prompt(user_text):
    # handles yes and no prompts
    answer = input(user_text)
    answer.strip()
    answer.lower()
    if answer == 'yes':
        return True
    elif answer == 'no':
        return False
    else:
        print("Please enter a valid response. yes or no\n")
        return binary_prompt(user_text)


def filepath_prompt(user_text):
    # prompts user for filepath and tests if it exists.
    # Returns [filepath, filename, and boolean of the files exists]
    # True file exists
    # False file doesn't exist
    file_path = input(user_text)
    # extract filename out of filepath
    filename_split = file_path.split('/')
    filename_split_2 = filename_split[-1].split('\\')
    try:
        f = open(file_path, 'r')
        f.close()
        return [file_path, filename_split_2[-1], True]
    except FileNotFoundError:
        return [file_path, filename_split_2[-1], False]


def prompt_credentials():
    # prompts user for username and password and returns [username, password]
    username = input("Username:\n")
    prompt = binary_prompt("Use {} as your username? yes or no\n".format(username))
    if prompt:
        pass
    else:
        return prompt_credentials()
    password = getpass()
    print("To prevent lockouts please re-enter your password\n")
    verify_password = getpass()
    if password == verify_password:
        return [username, password]
    else:
        print("Passwords do not match\n")
        return prompt_credentials()


async def ssh_connect(sort_dict):
    # takes in a sorted connection dictionary used to make ssh connections
    # returns our "thread_dict" with the format {device_name: connection_object}
    print("#"*20+"   TESTING   "+"#"*20)
    device_list = list(sort_dict)
    print(device_list)
    coroutine = [ConnectHandler(**sort_dict[device]) for device in device_list]
    print("#" * 20 + "   coroutine   " + "#" * 20+"\n")
    print(coroutine)
    print("\n")
    # threads = await asyncio.gather(*coroutine)
    threads = coroutine
    thread_dict = {device_list[i]: threads[i] for i in range(len(device_list))}
    return thread_dict


async def ssh_disconnect(thread_dict):
    # function that disconnects from each device
    device_list = list(thread_dict)
    print("Disconnecting from {}".format(device) for device in device_list)
    coroutine = [thread_dict[device].disconnect() for device in device_list]
    await asyncio.gather(*coroutine)


# async functions that interact with remote devices
async def send_exec_command(thread_dict, send_dict):
    # sends the command to each device
    # thread_dict is a dictionary containing ssh_connection object for its respective device
    device_list = list(thread_dict)
    coroutine = [thread_dict[device].send_command(**send_dict) for device in device_list]
    output_list = await asyncio.gather(*coroutine)
    output_dict = {device_list[i]: output_list[i] for i in range(len(device_list))}
    return output_dict


def main():
    print("#"*20+"    SET TRACE    "+"#"*20+"\n")
    #ipdb.set_trace()
    # set up our send arguments in here:
    # ssh setup
    # note need to run asyncio.run(function())
    thread_dict = asyncio.run(ssh_connect(sort_dict=device_dict))

    # send commands
    output = asyncio.run(send_exec_command(thread_dict=thread_dict, send_dict=exec_send_args))
    print(output)
    # close ssh connection
    ssh_disconnect(thread_dict)
    return None


if __name__ == "__main__":
    main()
