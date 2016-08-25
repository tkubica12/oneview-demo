# Ansible Oneview demo

This is Infrastructure as code demo of automation of infrastructure setup including compute, storage and interconnect resources managed via OneView, HPE Comware-based networking switches managed via HPE Comware Ansible modules, OS deployment via HPE ICsp and OS configuration with Ansible roles.

Currently this is work in progress, not all steps are implemented yet.

## Overall configuration

Desired state is described in config.yaml. Currently there is only networking, but it is used to configure both Blade server interconnects and network profiles as well as HPE ToR switch. Content should be self explanatory and you can easily add more networks, ports etc.

To run complete playbook use
'''
ansible-playbook -i hosts main.yaml
'''

OneView appliance connectivity details are in oneview-config.json.
ToR switch IP address and credentials is in hosts file.

Main playbook is leveraging roles which you can find in roles folder (see tasks subfolder for details of what they do).

## OneView networking

This role creates network profiles with proper names and VLAN IDs and create Uplink Set associated with networks and desired ports.

## ToR networking

This role configured ToR switch. Create VLANs, configure link aggregation interfaces (if required) and setup trunks (individual ports and/or link aggregation interfaces) to allow listed VLANs/Networks.
