# -*- coding: utf8 -*-
import os
import requests, json
from cloudfoundry_client.client import CloudFoundryClient

def loginCF(config):
    #cf login
    cf_endpoint = config.get('pcf_conf', 'endpoint')
    cf_user = config.get('pcf_conf', 'user')
    cf_passwd = config.get('pcf_conf', 'password')
    proxy = dict(http = os.environ.get('HTTP_PROXY', ''), https = os.environ.get('HTTPS_PROXY', ''))
    client = CloudFoundryClient(cf_endpoint, proxy = proxy, skip_verification = True)
    client.init_with_user_credentials(cf_user, cf_passwd)
    return client, client.service_information

def getServiceInfo(client, dbname):
    #get service guid, get space guid & org guid
    service_guid = -1
    for service in client.service_instances:
        if service['metadata']['guid'] == dbname:
            service_guid = service['metadata']['guid']
            space_guid = service['entity']['space_guid']
            for space in client.spaces:
                if space['metadata']['guid'] == space_guid:
                    org_guid = space['entity']['organization_guid']
    if service_guid == -1:
        return service_guid, 0, 0, 0
    #get application guiddb
    app_guid = -1
    for service_bind in client.service_bindings:
        if service_bind['entity']['service_instance_guid'] == service_guid:
            app_guid = service_bind['entity']['app_guid']

    return service_guid, app_guid, space_guid, org_guid

def toAbacus(postmsg, endpoint):
    headers = {'Content-Type': 'application/json'}
    measure_data = [{"measure": postmsg['measure_amount'],"quantity": postmsg['storage_size']}, \
                    {"measure": postmsg['measure_traffic'],"quantity": postmsg['transaction_count']},\
                    {"measure": 'count',"quantity": '1'}]
    post_data = {"start": postmsg['start_timestamp'],
                 "end": postmsg['end_timestamp'],
                 "organization_id": postmsg['org_guid'],
                 "space_id": postmsg['space_guid'],
                 "consumer_id": postmsg['app_guid'],
                 "resource_id": postmsg['db_storage'],
                 "plan_id": postmsg['plan_type'],
                 "resource_instance_id": postmsg['service_guid'],
                 "measured_usage": measure_data}
    postResult = requests.post(endpoint, headers=headers, data=json.dumps(post_data), verify=False)
    return postResult

def sizeNormalize(dbsize):
    if 'kB' in dbsize:
        intsize = int(dbsize.replace('kB','').strip()) * 1024
    elif 'MB' in dbsize:
        intsize = int(dbsize.replace('MB','').strip()) * 1024 *1024
    elif 'GB' in dbsize:
        intsize = int(dbsize.replace('GB','').strip()) * 1024 *1024 * 1024
    else:
        return -1
    return intsize

def log(fp, s):
    fp.write(s)
    print s
    return

def getVcapSpace():
    try:
        space = str(json.loads(os.environ['VCAP_APPLICATION'])["space_name"]).lower()
        if space != 'production' and space != 'stage' and space != 'develop':
            print "Invalid space name for postgresql host"
            exit(0)
    except:
        space = 'production'
    return space

