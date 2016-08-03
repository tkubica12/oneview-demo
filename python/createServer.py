#!/usr/bin/python

# Script to demonstrate OneView Python interaction
# Creating and booting one or more servers
# Tomas Kubica

import hpOneView as ov
import argparse
import hpOneView.profile as profile
import sys

# Let's just parse script inputs
parser = argparse.ArgumentParser(description='Creating servers OneView')
parser.add_argument('--ov-server', help='OneView IP address',
    dest='oneview_server', default='192.168.89.100')
parser.add_argument('--ov-user', help='OneView username',
    dest='oneview_user', default='Administrator')
parser.add_argument('--ov-password', help='OneView password',
    dest='oneview_password', default='HPEnet123')
parser.add_argument('--storage-pool', help='Storage pool name',
    dest='storage_pool',default='CPG-SSD')
parser.add_argument('--servers', help='Servers to be created',
    dest='servers', nargs='+', required=True)
parser.add_argument('--hardware', help='Hardware type',
    dest='hardware', default='BL460c Gen9 1')
parser.add_argument('--raid', dest='raid', required=False,
                    choices=['NONE', 'RAID0', 'RAID1'],
                    default='RAID1',
                    help='Specify RAID level as NONE, RAID0 or RAID1')
parser.add_argument('--drives', dest='drives',
                    default='2', help='Number of RAID drives')

args = parser.parse_args()

# Get connection and log into OneView
con = ov.connection(args.oneview_server)
login = {'userName':args.oneview_user,'password':args.oneview_password}
con.login(login)

# Get access to compute resources
compute =  ov.servers(con)

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

    # Prepare local storage profile
    localStorage = profile.make_local_storage_dict(
                            con.get(selectedServer['serverHardwareTypeUri']),
                            args.raid, True, True, 2)
    print localStorage
    sys.exit()



    # Create server profile
    print 'Creating profile of server', server
    result = compute.create_server_profile(name=server,
                                  serverHardwareUri=selectedServer['serverHardwareUri'],
                                  localStorageSettingsV3=localStorage)

    print 'Created profile %s on %s' % (server, selectedServer['serverHardwareName'])

    # Boot server
    print 'Booting server', server
    compute.set_server_powerstate(compute.get_server_by_name(selectedServer['serverHardwareName']), 'On')
    print
