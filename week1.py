#!/usr/bin/env python

import netmiko

# device setup dictionaries for lab
device_dict = {
'cisco3': {
    # 'comment': 'Cisco IOS-XE',
    'host': 'cisco3.lasthop.io',
    'snmp_port': 161,
    'ssh_port': 22,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'ios_xe'
},

'cisco': {
    # 'comment': 'Cisco IOS-XE',
    'host': 'cisco4.lasthop.io',
    'snmp_port': 161,
    'ssh_port': 22,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'ios_xe'
},

'arista1': {
    # 'comment': 'Arista_vEOS_switch',
    'host': 'arista1.lasthop.io',
    'ssh_port': 22,
    'eapi_port': 443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'arista'
},

'arista2': {
    # 'comment': 'Arista_vEOS_switch',
    'host': 'arista2.lasthop.io',
    'ssh_port': 22,
    'eapi_port': 443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'arista'
},

'arista3': {
    # 'comment': 'Arista_vEOS_switch',
    'host': 'arista3.lasthop.io',
    'ssh_port': 22,
    'eapi_port': 443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'arista'
},

'arista4': {
    # 'comment': 'Arista_vEOS_switch',
    'host': 'arista4.lasthop.io',
    'ssh_port': 22,
    'eapi_port': 443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'arista'
},

'srx2': {
    # 'comment': 'Juniper_SRX',
    'host': 'srx2.lasthop.io',
    'ssh_port': 22,
    'netconf_port': 830,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'juniper'
},

'nxos1': {
    # 'comment': 'NX-OSv Switch',
    'host': 'nxos1.lasthop.io',
    'ssh_port': 22,
    'nxapi_port': 8443,
    'username': 'pyclass',
    'password': '88newclass',
},

'nxos2': {
    # 'comment': 'NX-OSv Switch',
    'host': 'nxos2.lasthop.io',
    'ssh_port': 22,
    'nxapi_port': 8443,
    'username': 'pyclass',
    'password': '88newclass',
    'device_type': 'nxos'
}
}