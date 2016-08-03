#!/usr/bin/python

import hpOneView as ov
import argparse

parser = argparse.ArgumentParser(description='Deleting storage Volumes via OneView')
parser.add_argument('--ov-server', help='OneView IP address',
    dest='oneview_server', default='192.168.89.100')
parser.add_argument('--ov-user', help='OneView username',
    dest='oneview_user', default='Administrator')
parser.add_argument('--ov-password', help='OneView password',
    dest='oneview_password', default='HPEnet123')
parser.add_argument('--storage-pool', help='Storage pool name',
    dest='storage_pool', default='CPG-SSD')
parser.add_argument('--volume', help='Volume to be cloned',
    dest='volume', required=True)
parser.add_argument('--clone', help='Name of cloned volume',
    dest='clone', required=True)

args = parser.parse_args()

con = ov.connection(args.oneview_server)
login = {'userName':args.oneview_user,'password':args.oneview_password}
con.login(login)

storage = ov.storage(con)
pools = storage.get_storage_pools()
for pool in pools['members']:
    if pool['name'] == args.storage_pool:
        storagePoolUri = pool['uri']
        existing_volumes = storage.get_storage_volumes()
        for existing_volume in existing_volumes['members']:
            if existing_volume['name'] == volume:
                print 'Creating snapshot of volume: ', volume
                storage.remove_storage_volume(existing_volume)
