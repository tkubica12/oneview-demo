# Ansible Oneview demo

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

This role creates network profiles with proper names and VLAN IDs and create Uplink Set associated with networks and desired ports.

## ToR networking

This role configured ToR switch. Create VLANs, configure link aggregation interfaces (if required) and setup trunks (individual ports and/or link aggregation interfaces) to allow listed VLANs/Networks.

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

TASK [ov-networking : Create map with facts about interconnects] ***************
ok: [localhost] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/2', u'GigabitEtherneTASK [ov-networking : Map port configurations to JSON array] *******************
ok: [localhost]

TASK [ov-networking : Get Logical Interconnect URI] ****************************
ok: [localhost]

TASK [ov-networking : Ensure that the Uplink Set with our Networks is present] *
changed: [localhost]

PLAY [Top-of-rack networking] **************************************************

TASK [tor-networking : Ensure that VLANs exist] ********************************
ok: [192.168.56.10] => (item={u'id': 101, u'name': u'Prod-101'})
ok: [192.168.56.10] => (item={u'id': 102, u'name': u'Prod-102'})
ok: [192.168.56.10] => (item={u'id': 103, u'name': u'Dev-103'})

TASK [tor-networking : Ensure link aggregation is configured] ******************
changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/2', u'GigabitEthernet 1/0/3']})
changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/4', u'GigabitEthernet 1/0/5']})

TASK [tor-networking : Create permited VLANs string] ***************************
ok: [192.168.56.10]

TASK [tor-networking : Ensure that VLANs are configured on standalone ports] ***
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/2'))
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/3'))
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/4'))
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/5'))

TASK [tor-networking : Ensure that VLANs are configured on link aggregattion interfaces] ***
changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/2', u'GigabitEthernet 1/0/3']})
changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/4', u'GigabitEthernet 1/0/5']})

TASK [tor-networking : Save switch configuration] ******************************
changed: [192.168.56.10]

PLAY RECAP *********************************************************************
192.168.56.10              : ok=5    changed=3    unreachable=0    failed=0   
localhost                  : ok=7    changed=1    unreachable=0    failed=0   

t 1/0/3']})
ok: [localhost] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/4', u'GigabitEthernet 1/0/5']})

TASK [ov-networking : Build port configurations] *******************************
ok: [localhost] => ...
...

TASK [ov-networking : Map port configurations to JSON array] *******************
ok: [localhost]

TASK [ov-networking : Get Logical Interconnect URI] ****************************
ok: [localhost]

TASK [ov-networking : Ensure that the Uplink Set with our Networks is present] *
changed: [localhost]

PLAY [Top-of-rack networking] **************************************************

TASK [tor-networking : Ensure that VLANs exist] ********************************
ok: [192.168.56.10] => (item={u'id': 101, u'name': u'Prod-101'})
ok: [192.168.56.10] => (item={u'id': 102, u'name': u'Prod-102'})
ok: [192.168.56.10] => (item={u'id': 103, u'name': u'Dev-103'})

TASK [tor-networking : Ensure link aggregation is configured] ******************
changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/2', u'GigabitEthernet 1/0/3']})
changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/4', u'GigabitEthernet 1/0/5']})

TASK [tor-networking : Create permited VLANs string] ***************************
ok: [192.168.56.10]

TASK [tor-networking : Ensure that VLANs are configured on standalone ports] ***
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/2'))
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/3'))
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/4'))
skipping: [192.168.56.10] => (item=({u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'ports': [u'X2', u'X4']}, u'GigabitEthernet 1/0/5'))

TASK [tor-networking : Ensure that VLANs are configured on link aggregattion interfaces] ***
changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 1, u'module': u'Encl1, interconnect 1', u'switchports': [u'GigabitEthernet 1/0/2', u'GigabitEthernet 1/0/3']})
changed: [192.168.56.10] => (item={u'ports': [u'X2', u'X4'], u'switch_link_aggregation_group': 2, u'module': u'Encl1, interconnect 2', u'switchports': [u'GigabitEthernet 1/0/4', u'GigabitEthernet 1/0/5']})

TASK [tor-networking : Save switch configuration] ******************************
changed: [192.168.56.10]

PLAY RECAP *********************************************************************
192.168.56.10              : ok=5    changed=3    unreachable=0    failed=0   
localhost                  : ok=7    changed=1    unreachable=0    failed=0   

```
