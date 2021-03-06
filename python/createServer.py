#!/usr/bin/python

# Script to demonstrate OneView Python interaction
# Creating and booting one or more servers
# Tomas Kubica

import hpOneView as ov
import hpOneView.profile as profile
import argparse

# Let's just parse script inputs
parser = argparse.ArgumentParser(description='Creating servers OneView')
parser.add_argument('--ov-server', help='OneView IP address',
    dest='oneview_server', default='192.168.89.100')
parser.add_argument('--ov-user', help='OneView username',
    dest='oneview_user', default='Administrator')
parser.add_argument('--ov-password', help='OneView password',
    dest='oneview_password', default='HPEnet123')
parser.add_argument('--servers', help='Servers to be created',
    dest='servers', nargs='+', required=True)
parser.add_argument('--hardware', help='Hardware type',
    dest='hardware', default='BL460c Gen9 1')
parser.add_argument('--connection', help='Network profile',
    dest='connection', required=False)
parser.add_argument('--raid', dest='raid', required=False,
    choices=['NONE', 'RAID0', 'RAID1'],
    help='Choose raid level on local storage')
parser.add_argument('--drives', dest='drives', required=False,
    help='Number of local storage disks')

args = parser.parse_args()

# Get connection and log into OneView
con = ov.connection(args.oneview_server)
login = {'userName':args.oneview_user,'password':args.oneview_password}
con.login(login)

# Get access to compute and network resources
compute =  ov.servers(con)
net = ov.networking(con)

selectedServer = ''

# We will loop over servers specified in input
print 'Creating servers...'
for server in args.servers:

    # Get list of unassigned servers and select first available
    unassignedServers = compute.get_available_servers()
    for unassignedServer in unassignedServers['targets']:
        if unassignedServer['serverHardwareTypeName'] == args.hardware:
            selectedServer = unassignedServer
            break

    # Check whether server is power on and if yes, power off
    if selectedServer['powerState'] != 'Off':
        print 'Shutting down server', selectedServer['serverHardwareName']
        compute.set_server_powerstate(
                   compute.get_server_by_name(selectedServer['serverHardwareName']),
                  'Off', force=True, blocking=True)

    # Create connection  profile
    if args.connection:
        networks = net.get_enet_networks()
        netw = None
        for network in networks:
            if network['name'] == args.connection:
                netw = network
                break
        connectionProfile = ov.common.make_ProfileConnectionV4(cid=1,
                                                               name='My_connection',
                                                               networkUri=netw['uri'],
                                                               functionType='Ethernet',
                                                               profileTemplateConnection=True)

    # Create local storage profile
    if args.raid:
        storageProfile = profile.make_local_storage_dict(sht=con.get(selectedServer['serverHardwareUri']),
                                                         raidlevel=args.raid,
                                                         lboot=False,
                                                         init_storage=True,
                                                         num=args.drives,
                                                         drive_name='MyDrive')

    # Create server profile
    print 'Creating profile of server', server
    if (args.raid and args.connection):
        result = compute.create_server_profile(name=server,
                                      serverHardwareUri=selectedServer['serverHardwareUri'],
                                      localStorageSettingsV3=storageProfile,
                                      profileConnectionV4=[connectionProfile])
    elif (args.raid):
        result = compute.create_server_profile(name=server,
                                      serverHardwareUri=selectedServer['serverHardwareUri'],
                                      localStorageSettingsV3=storageProfile)
    elif (args.connection):
        result = compute.create_server_profile(name=server,
                                      serverHardwareUri=selectedServer['serverHardwareUri'],
                                      profileConnectionV4=[connectionProfile])
    else:
        result = compute.create_server_profile(name=server,
                                      serverHardwareUri=selectedServer['serverHardwareUri'])

    print 'Created profile %s on %s' % (server, selectedServer['serverHardwareName'])

    # Boot server
    print 'Booting server', server
    compute.set_server_powerstate(compute.get_server_by_name(selectedServer['serverHardwareName']), 'On')
    print
