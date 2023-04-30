#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Daniel Podwysocki <https://github.com/danielpodwysocki>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: pfsense_virtual_ip
version_added: 0.1.0
author: Daniel Podwysocki (@danielpodwysocki)
short_description: Manage pfSense virtual IPs.
description:
  - Manage pfSense virtual IPs.
notes:
options:
  state:
    description: State in which to leave the virtual IP.
    choices: [ "present", "absent" ]
    default: present
    type: str
  vip_type:
    description: Type of virtual IP.
    choices: [ "ipalias", "carp", "proxyarp", "other" ]
    default: ipalias
    type: str
  vip_password:
    description: Password for CARP virtual IP, for the VHID group.
    required: false
    type: str
  vip_vhid_group:
    description: VHID group for CARP virtual IP.
    required: false
    type: int
  vip_vhid_advertise_frequency_base:
    description: Advertise frequency for CARP virtual IP.
    required: false
    type: int
  vip_vhid_advertise_frequency_skew:
    description: Advertise frequency skew for CARP virtual IP.
    required: false
    type: int
  vip_expand:
    description: Expand this into IPs on NAT lists. Only applies to IP Alias and Proxy ARP types.
    default: true
    type: bool
  descr:
    description: Description of the VIP. For reference only.
    required: false
    type: str
  ipv4_address:
    description: IPv4 Address.
    required: false
    type: str
  ipv4_prefixlen:
    description: IPv4 subnet prefix length. This is the subnet in which the interface resides.
    required: false
    default: 24
    type: int
  ipv6_address:
    description: IPv6 Address.
    required: false
    type: str
  ipv6_prefixlen:
    description: IPv6 subnet prefix length. This is the subnet in which the interface resides.
    required: false
    default: 128
    type: int
  ipv6_gateway:
    description: IPv6 gateway for this interface.
    required: false
    type: str
"""

EXAMPLES = """
- name: Add interface
  pfsense_interface:
    descr: voice
    interface: mvneta0.100
    enable: True

- name: Remove interface
  pfsense_interface:
    state: absent
    descr: voice
    interface: mvneta0.100
"""

RETURN = """
commands:
    description: The set of commands that would be pushed to the remote device (if pfSense had a CLI).
    returned: always
    type: list
    sample: [
        "create interface 'voice', port='mvneta0.100', speed_duplex='autoselect', enable='True'",
        "delete interface 'voice'"
    ]
ifname:
    description: The pseudo-device name of the interface.
    returned: always
    type: str
    sample: opt1
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfsensible.core.plugins.module_utils.virtual_ip import (
    PFSenseVirtualIPModule,
    INTERFACE_ARGUMENT_SPEC,
    INTERFACE_REQUIRED_IF,
    INTERFACE_MUTUALLY_EXCLUSIVE,
)


def main():
    module = AnsibleModule(
        argument_spec=INTERFACE_ARGUMENT_SPEC,
        required_if=INTERFACE_REQUIRED_IF,
        mutually_exclusive=INTERFACE_MUTUALLY_EXCLUSIVE,
        supports_check_mode=True,
    )

    pfmodule = PFSenseInterfaceModule(module)
    pfmodule.run(module.params)
    pfmodule.commit_changes()


if __name__ == "__main__":
    main()
