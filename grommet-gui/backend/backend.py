from bottle import route, run, get, post, request, response
import json
import hpOneView as ov
import os

username = os.getenv('OV_USERNAME', 'Administrator')
password = os.getenv('OV_PASSWORD', 'HPEnet123')
oneview_server = os.getenv('OV_SERVER', '192.168.89.100')
storage_pool = os.getenv('OV_STORAGE_POOL', 'CPG-SSD')

@post('/volume')
def volume():
    data = request.body.read()
    volume = json.loads(data)['volume_name']

    # Get connection and log into OneView
    con = ov.connection(oneview_server)
    login = {'userName':username,'password':password}
    con.login(login)

    # Get access to storage resources
    storage = ov.storage(con)
    pools = storage.get_storage_pools()
    for pool in pools['members']:

        # Find specified storage pool
        if pool['name'] == storage_pool:
            storagePoolUri = pool['uri']
            newvolume = ov.common.make_storage_volume(volume,
                                                 102410241024,
                                                 True,
                                                 storagePoolUri,
                                                 'Created via script',
                                                 'thin')
            result = storage.add_storage_volume(newvolume)

    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.status = 200
    print json.dumps({'state': result['state']})
    return json.dumps({'state': result['state']})


@get('/volumes')
def volume():
    count = 0

    # Get connection and log into OneView
    con = ov.connection(oneview_server)
    login = {'userName':username,'password':password}
    con.login(login)

    # Get access to storage resources
    storage = ov.storage(con)
    pools = storage.get_storage_pools()
    for pool in pools['members']:

        # Find specified storage pool
        if pool['name'] == storage_pool:
            existing_volumes = storage.get_storage_volumes()

    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.status = 200
    print json.dumps({'count': existing_volumes['count']})
    return json.dumps({'count': existing_volumes['count']})


run(host='0.0.0.0', port=3000, debug=True)
