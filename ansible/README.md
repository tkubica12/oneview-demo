d # Ansible Oneview demo

This is Infrastructure as code demo of automation of infrastructure setup including compute, storage and interconnect resources managed via OneView, HPE Comware-based networking switches managed via HPE Comware Ansible modules, OS deployment via HPE ICsp and OS configuration with Ansible roles.

Currently this is work in progress, not all steps are implemented yet.

## Environment setup

You need to install Ansible, OneView modules, Comware Python library and Comware Ansible modules in order to run this. Details how to do it are in install.sh

## Overall configuration

Desired state is described in config.yaml. Currently there is only networking, but it is used to configure both Blade server interconnects and network profiles as well as HPE ToR switch. Content should be self explanatory and you can easily add more networks, ports etc.

To run complete playbook use
```
ansible-playbook -i hosts main.yaml
```

OneView appliance connectivity details are in oneview-config.json.
ToR switch IP address and credentials is in hosts file.

Main playbook is leveraging roles which you can find in roles folder (see tasks subfolder for details of what they do).

## OneView networking

This role creates network profiles with proper names and VLAN IDs, assign networks to logical interconnect group and create Uplink Set associated with networks and interconnects and desired ports.

## ToR networking

This role configured ToR switch. Create VLANs, configure link aggregation interfaces (if required) and setup trunks (individual ports and/or link aggregation interfaces) to allow listed VLANs/Networks. This is currently limited to single logical switch (standalone device or IRF cluster).

## Server profile

This role creates server templates based on config.yaml and then creates server profiles as listed in config.yaml.

## Example output

This is how Ansible output looks.

```
$ ansible-playbook -i hosts main.yaml

PLAY [Blade networking] ********************************************************

TASK [ov-networking : Ensure that Networks exist] ******************************
ok: [localhost] => (item={u'id': 101, u'name': u'Prod-101'})
ok: [localhost] => (item={u'id': 102, u'name': u'Prod-102'})
ok: [localhost] => (item={u'id': 103, u'name': u'Dev-103'})

TASK [ov-networking : Store network URIs in list] ******************************
ok: [localhost]

TASK [ov-networking : Ensure networks are present on Logical interconnect group] ***
changed: [localhost]

TASK [ov-networking : Ensure UplinkSets are configured] ************************
included: /home/hpe/oneview-demo/ansible/roles/ov-networking/tasks/uplinksets.yaml for localhost
included: /home/hpe/oneview-demo/ansible/roles/ov-networking/tasks/uplinksets.yaml for localhost

TASK [ov-networking : Create map with facts about interconnects] ***************
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

ok: [localhost] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/2', u'GigabitEthernet 1/0/3']})
ok: [localhost] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/4', u'GigabitEthernet 1/0/5']})

TASK [ov-networking : Build port configurations] *******************************
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

ok: [localhost] => ...

TASK [ov-networking : Map port configurations to JSON array] *******************
ok: [localhost]

TASK [ov-networking : Get Logical Interconnect URI] ****************************
ok: [localhost]

TASK [ov-networking : Ensure that the Uplink Set with Networks is present] *****
changed: [localhost]

TASK [ov-networking : Create map with facts about interconnects] ***************
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

ok: [localhost] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 3, u'module': u'Encl2, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/6', u'GigabitEthernet 1/0/7']})
ok: [localhost] => (item={u'ports': [u'X2', u'X4'], u'module': u'Encl2, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/8', u'GigabitEthernet 1/0/9']})

TASK [ov-networking : Build port configurations] *******************************
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

ok: [localhost] => ...

TASK [ov-networking : Map port configurations to JSON array] *******************
ok: [localhost]

TASK [ov-networking : Get Logical Interconnect URI] ****************************
ok: [localhost]

TASK [ov-networking : Ensure that the Uplink Set with Networks is present] *****
changed: [localhost]

PLAY [Top-of-rack networking] **************************************************

TASK [tor-networking : Ensure that VLANs exist] ********************************
ok: [192.168.56.10] => (item={u'id': 101, u'name': u'Prod-101'})
ok: [192.168.56.10] => (item={u'id': 102, u'name': u'Prod-102'})
ok: [192.168.56.10] => (item={u'id': 103, u'name': u'Dev-103'})

TASK [tor-networking : Create permited VLANs string] ***************************
ok: [192.168.56.10]

TASK [tor-networking : Ensure ports are configured] ****************************
included: /home/hpe/oneview-demo/ansible/roles/tor-networking/tasks/ports.yaml for 192.168.56.10
included: /home/hpe/oneview-demo/ansible/roles/tor-networking/tasks/ports.yaml for 192.168.56.10

TASK [tor-networking : Ensure link aggregation is configured] ******************
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/2', u'GigabitEthernet 1/0/3']})
changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/4', u'GigabitEthernet 1/0/5']})

TASK [tor-networking : Ensure that VLANs are configured on standalone ports] ***
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/2'))
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/3'))
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/4'))
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/5'))

TASK [tor-networking : Ensure that VLANs are configured on link aggregattion interfaces] ***
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/2', u'GigabitEthernet 1/0/3']})
changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/4', u'GigabitEthernet 1/0/5']})

TASK [tor-networking : Ensure link aggregation is configured] ******************
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 3, u'module': u'Encl2, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/6', u'GigabitEthernet 1/0/7']})
skipping: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'module': u'Encl2, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/8', u'GigabitEthernet 1/0/9']})

TASK [tor-networking : Ensure that VLANs are configured on standalone ports] ***
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 3, u'module': u'Encl2, interconnect 1', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/6'))
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 3, u'module': u'Encl2, interconnect 1', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/7'))
changed: [192.168.56.10] => (item=({u'ports': [u'X2', u'X4'], u'module': u'Encl2, interconnect 2'}, u'GigabitEthernet 1/0/8'))
changed: [192.168.56.10] => (item=({u'ports': [u'X2', u'X4'], u'module': u'Encl2, interconnect 2'}, u'GigabitEthernet 1/0/9'))

TASK [tor-networking : Ensure that VLANs are configured on link aggregattion interfaces] ***
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 3, u'module': u'Encl2, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/6', u'GigabitEthernet 1/0/7']})
skipping: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'module': u'Encl2, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/8', u'GigabitEthernet 1/0/9']})

TASK [tor-networking : Save switch configuration] ******************************
changed: [192.168.56.10]

PLAY [Servers] *****************************************************************

TASK [server-profiles : Ensure server profiles templates are presentt] *********
included: /home/hpe/oneview-demo/ansible/roles/server-profiles/tasks/profile-template.yaml for localhost
included: /home/hpe/oneview-demo/ansible/roles/server-profiles/tasks/profile-template.yaml for localhost

TASK [server-profiles : Gather facts about a Enclosure Group by name] **********
ok: [localhost]

TASK [server-profiles : Gather facts about Ethernet networks] ******************
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

ok: [localhost] => (item=Prod-101)
ok: [localhost] => (item=Prod-102)

TASK [server-profiles : Prepare individual JSON objects for Ethernet networks] *
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

ok: [localhost] => (item={u'changed': False, '_ansible_no_log': False, '_ansible_item_result': True, 'item': u'Prod-101', 'invocation': {'module_name': u'oneview_ethernet_network_facts', u'module_args': {u'config': u'oneview-config.json', u'name': u'Prod-101'}}, u'ansible_facts': {u'ethernet_networks': [{u'status': u'OK', u'category': u'ethernet-networks', u'ethernetNetworkType': u'Tagged', u'description': None, u'name': u'Prod-101', u'created': u'2016-08-23T05:17:05.557Z', u'uri': u'/rest/ethernet-networks/a1021dc9-f76d-4bc8-bfb8-ceaa49591477', u'vlanId': 101, u'modified': u'2016-08-23T05:17:05.558Z', u'fabricUri': u'/rest/fabrics/a915e022-7ebb-4add-ad14-d88ef088d421', u'eTag': u'c580dc99-6d4f-4b41-aec3-a04c4a987b98', u'purpose': u'General', u'state': u'Active', u'connectionTemplateUri': u'/rest/connection-templates/6386824a-6090-431c-b8c2-fc4d5e711cd7', u'type': u'ethernet-networkV3', u'smartLink': True, u'privateNetwork': False}]}})
ok: [localhost] => (item={u'changed': False, '_ansible_no_log': False, '_ansible_item_result': True, 'item': u'Prod-102', 'invocation': {'module_name': u'oneview_ethernet_network_facts', u'module_args': {u'config': u'oneview-config.json', u'name': u'Prod-102'}}, u'ansible_facts': {u'ethernet_networks': [{u'status': u'OK', u'category': u'ethernet-networks', u'ethernetNetworkType': u'Tagged', u'description': None, u'name': u'Prod-102', u'created': u'2016-08-23T05:17:06.091Z', u'uri': u'/rest/ethernet-networks/d49d4a7d-2a0f-4534-a9e3-622e8844ab19', u'vlanId': 102, u'modified': u'2016-08-23T05:17:06.093Z', u'fabricUri': u'/rest/fabrics/a915e022-7ebb-4add-ad14-d88ef088d421', u'eTag': u'ac665bd4-5fa1-40b4-a1fc-eef273230c9f', u'purpose': u'General', u'state': u'Active', u'connectionTemplateUri': u'/rest/connection-templates/a8914e9b-51ba-4e22-a611-d45ce19ef224', u'type': u'ethernet-networkV3', u'smartLink': True, u'privateNetwork': False}]}})

TASK [server-profiles : Map Ethernet configurations to JSON array] *************
ok: [localhost]

TASK [server-profiles : Ensure server profile template is present] *************
changed: [localhost]

TASK [server-profiles : Gather facts about a Enclosure Group by name] **********
ok: [localhost]

TASK [server-profiles : Gather facts about Ethernet networks] ******************
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

ok: [localhost] => (item=Dev-103)

TASK [server-profiles : Prepare individual JSON objects for Ethernet networks] *
 [WARNING]: The loop variable 'item' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable
collisions and unexpected behavior.

ok: [localhost] => (item={u'changed': False, '_ansible_no_log': False, '_ansible_item_result': True, 'item': u'Dev-103', 'invocation': {'module_name': u'oneview_ethernet_network_facts', u'module_args': {u'config': u'oneview-config.json', u'name': u'Dev-103'}}, u'ansible_facts': {u'ethernet_networks': [{u'status': u'OK', u'category': u'ethernet-networks', u'ethernetNetworkType': u'Tagged', u'description': None, u'name': u'Dev-103', u'created': u'2016-08-23T05:17:06.590Z', u'uri': u'/rest/ethernet-networks/edbfc0b8-0b35-4316-a247-9790ec69d0ef', u'vlanId': 103, u'modified': u'2016-08-23T05:17:06.591Z', u'fabricUri': u'/rest/fabrics/a915e022-7ebb-4add-ad14-d88ef088d421', u'eTag': u'c9deae72-42e3-4899-857a-325488eaca90', u'purpose': u'General', u'state': u'Active', u'connectionTemplateUri': u'/rest/connection-templates/7b30af86-5829-41df-baf4-0b2d44062962', u'type': u'ethernet-networkV3', u'smartLink': True, u'privateNetwork': False}]}})

TASK [server-profiles : Map Ethernet configurations to JSON array] *************
ok: [localhost]

TASK [server-profiles : Ensure server profile template is present] *************
changed: [localhost]

TASK [server-profiles : Ensure server profiles are present] ********************
ok: [localhost] => (item={u'profile': u'DB_servers', u'name': u'My_DB_1'})
ok: [localhost] => (item={u'profile': u'DB_servers', u'name': u'My_DB_2'})
ok: [localhost] => (item={u'profile': u'APP_servers', u'name': u'My_APP_1'})
ok: [localhost] => (item={u'profile': u'APP_servers', u'name': u'My_APP_2'})

PLAY RECAP *********************************************************************
192.168.56.10              : ok=10   changed=6    unreachable=0    failed=0   
localhost                  : ok=28   changed=5    unreachable=0    failed=0 
```
