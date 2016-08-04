#!/usr/bin/python

# Script to demonstrate OneView Python interaction
# Deleting one or more volumes
# Tomas Kubica

import hpOneView as ov
import argparse

# Let's just parse script inputs
parser = argparse.ArgumentParser(description='Deleting storage Volumes via OneView')
parser.add_argument('--ov-server', help='OneView IP address',
    dest='oneview_server', default='192.168.89.100')
parser.add_argument('--ov-user', help='OneView username',
    dest='oneview_user', default='Administrator')
parser.add_argument('--ov-password', help='OneView password',
    dest='oneview_password', default='HPEnet123')
parser.add_argument('--storage-pool', help='Storage pool name',
    dest='storage_pool', default='CPG-SSD')
parser.add_argument('--volumes', help='Volumes to be created',
    dest='volumes', nargs='+', required=True)

args = parser.parse_args()

# Get connection and log into OneView
con = ov.connection(args.oneview_server)
login = {'userName':args.oneview_user,'password':args.oneview_password}
con.login(login)

# Get access to storage resources
storage = ov.storage(con)
pools = storage.get_storage_pools()
for pool in pools['members']:

    # Find specified storage pool
    if pool['name'] == args.storage_pool:
        storagePoolUri = pool['uri']
        existing_volumes = storage.get_storage_volumes()

        # Loop throw volumes specified in input
        for vol in args.volumes:

            # Loop throw existing volumes
            for existing_volume in existing_volumes['members']:

                # Is this volume we want to remove?
                if existing_volume['name'] == vol:

                    # Remove volume
                    print 'Removing Storage Volume: ', existing_volume['name']
                    storage.remove_storage_volume(existing_volume)
