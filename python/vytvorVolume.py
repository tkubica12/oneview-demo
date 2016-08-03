#!/usr/bin/python

# Script to demonstrate OneView Python interaction
# Creating one or more volumes
# Tomas Kubica

import hpOneView as ov
import argparse

# Let's just parse script inputs
parser = argparse.ArgumentParser(description='Creating storage Volumes via OneView')
parser.add_argument('--ov-server', help='OneView IP address',
    dest='oneview_server', default='192.168.89.100')
parser.add_argument('--ov-user', help='OneView username',
    dest='oneview_user', default='Administrator')
parser.add_argument('--ov-password', help='OneView password',
    dest='oneview_password', default='HPEnet123')
parser.add_argument('--storage-pool', help='Storage pool name',
    dest='storage_pool',default='CPG-SSD')
parser.add_argument('--volumes', help='Volumes to be created',
    dest='volumes', nargs='+', required=True)
parser.add_argument('--volume-size', help='Volume size',
    dest='volume_size', default=2)
parser.add_argument('--volume-sharing', action='store_true',
    dest='volume_sharing')
parser.add_argument('--volume-provisioning', help='Volume provisioning',
    dest='volume_provisioning', default='Thin')

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

        # Loop throw volumes scpecified in input
        for vol in args.volumes:

            # Create volumes
            print 'Adding volume: ', vol
            volume = ov.common.make_storage_volume(vol,
                                                 int(args.volume_size)*1024*1024*1024,
                                                 args.volume_sharing,
                                                 storagePoolUri,
                                                 'Created via script',
                                                 args.volume_provisioning)
            result = storage.add_storage_volume(volume)
            if 'deviceVolumeName' in result:
                print 'Name:                 ', result['name']
                print 'Type:                 ', result['type']
                print 'State:                ', result['state']
                print 'Allocated Capacity:   ', result['allocatedCapacity']
                print 'Provisioned Capacity: ', result['provisionedCapacity']
                print
            else:
                print result
