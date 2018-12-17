import unittest
import os, sys, time
import psycopg2
import ConfigParser
from uuid import UUID
import requests, json
from cloudfoundry_client.client import CloudFoundryClient
from apis import getServiceInfo, log

# read configurations
config = ConfigParser.ConfigParser()
config.read("configs.ini")

#postgres connection
user = config.get('postgresql_conf', 'admin')
passwd = config.get('postgresql_conf', 'password')
dbname = config.get('postgresql_conf', 'dbname')
port = config.get('postgresql_conf', 'port')
try:
    space = str(json.loads(os.environ['VCAP_APPLICATION'])["space_name"]).lower()
    if space != 'production' and space != 'stage' and space != 'develop':
        print "Invalid space name for postgresql host"
        exit(0)
except:
    space = 'production'
host = config.get('postgresql_conf', 'host_' + space)
postgres_certification = 'dbname=' + dbname + ' user=' + user + ' password=' + passwd + ' host=' + host + ' port=' + port

#cf login
cf_endpoint = config.get('pcf_conf', 'endpoint')
cf_user = config.get('pcf_conf', 'user')
cf_passwd = config.get('pcf_conf', 'password')
proxy = dict(http = os.environ.get('HTTP_PROXY', ''), https = os.environ.get('HTTPS_PROXY', ''))

def cf_connection(cf_user, cf_passwd):
    client = CloudFoundryClient(cf_endpoint, proxy = proxy, skip_verification = True)
    client.init_with_user_credentials(cf_user, cf_passwd)

#using dbname to get cf info.
def dbname_get_cf_info(postgres_certification, cf_user, cf_passwd):
    client = CloudFoundryClient(cf_endpoint, proxy = proxy, skip_verification = True)
    client.init_with_user_credentials(cf_user, cf_passwd)
    sql_dbnames = 'SELECT datname FROM pg_database WHERE datistemplate = false;'
    conn = psycopg2.connect(postgres_certification)
    cur = conn.cursor()
    cur.execute(sql_dbnames)
    dbnames = cur.fetchall()
    conn.commit()
    for i in dbnames:
        if i[0] != 'template0' and i[0] != 'template1' and i[0] != 'postgres':
            getServiceInfo(client, i[0])

# send data to Abacus
def toAbacus(endpoint):
    headers = {'Content-Type': 'application/json'}
    measure_data = [{"measure": 'storage',"quantity": '10'},
                    {"measure": 'transaction',"quantity": '100'},
                    {"measure": 'count',"quantity": '1'}]
    post_data = {"start": int(time.time()) * 1000,
                 "end": int(time.time()) * 1000 + 100,
                 "organization_id": '00000000-0000-0000-0000-000000000000',
                 "space_id": '00000000-0000-0000-0000-000000000000',
                 "consumer_id": '00000000-0000-0000-0000-000000000000',
                 "resource_id": 'postgresql',
                 "plan_id": 'basic',
                 "resource_instance_id": '00000000-0000-0000-0000-000000000000',
                 "measured_usage": measure_data}
    return requests.post(endpoint, headers=headers, data=json.dumps(post_data), verify=False)

def sizeNormalize():
    sql_dbnames = 'SELECT datname FROM pg_database WHERE datistemplate = false;'
    sql_size = 'SELECT pg_size_pretty(pg_database_size(\'mydb\'));'
    conn = psycopg2.connect(postgres_certification)
    cur = conn.cursor()
    cur.execute(sql_dbnames)
    dbnames = cur.fetchall()
    conn.commit()
    for i in dbnames:
        if i[0] != 'template0' and i[0] != 'template1' and i[0] != 'postgres':
            cur.execute(sql_size.replace('mydb', str(i[0])))
            dbsize = cur.fetchone()
            conn.commit()
            if 'kB' in str(dbsize):
                pass
            elif 'MB' in str(dbsize):
                pass
            elif 'GB' in str(dbsize):
                pass
            else:
                return False
    return True

class allTests(unittest.TestCase):

    def test_durationtime(self):
        self.assertTrue(int(config.get('dbmetering_conf', 'durationtime')) > 0)
    def test_detaillog(self):
        self.assertTrue(config.get('dbmetering_conf', 'detaillog') == 'enable' or config.get('dbmetering_conf', 'detaillog') == 'disable')
    def test_postgresql_connection(self):
        self.assertRaises(psycopg2.connect(postgres_certification))
    def test_cf_login(self):
        self.assertRaises(cf_connection(cf_user, cf_passwd))
    def test_dbname_get_cf_info(self):
        self.assertRaises(dbname_get_cf_info(postgres_certification,cf_user, cf_passwd))
    def test_abcus_connection(self):
        self.assertTrue(str(toAbacus(config.get('abacus_conf', 'endpoint_' + space)).status_code) == '201')
    def test_dbsize_normalization(self):
        self.assertTrue(sizeNormalize())
    def test_write_log(self):
        self.assertRaises(log(open('log.txt', 'a'), ''))

if __name__ == '__main__':
    unittest.main()