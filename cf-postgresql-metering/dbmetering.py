# -*- coding: utf8 -*-
import os, sys, time
import psycopg2
import ConfigParser
from uuid import UUID
from apis import *

#dbname sql & dbsize sql & dbtrans sql
###########################################################################################################
sql_dbnames = 'SELECT datname FROM pg_database WHERE datistemplate = false;'
sql_size = 'SELECT pg_size_pretty(pg_database_size(\'mydb\'));'
sql_trans = 'SELECT xact_commit+xact_rollback FROM pg_stat_database WHERE datname = \'mydb\';'
###########################################################################################################

# read configurations
config = ConfigParser.ConfigParser()
config.read("configs.ini")

#postgres login certification
user = config.get('postgresql_conf', 'admin')
passwd = config.get('postgresql_conf', 'password')
dbname = config.get('postgresql_conf', 'dbname')
port = config.get('postgresql_conf', 'port')
space = getVcapSpace()
host = config.get('postgresql_conf', 'host_' + space)
postgres_certification = 'dbname=' + dbname + ' user=' + user + ' password=' + passwd + ' host=' + host + ' port=' + port

#set  duration time
duration_time = 0
if not str(config.get('dbmetering_conf', 'durationtime')).isdigit() or int(config.get('dbmetering_conf', 'durationtime')) < 1:
    print "dbmetering duration time (sec) is a integer and more than 0"
    exit(0)
else:
    duration_time = int(config.get('dbmetering_conf', 'durationtime'))
currentTime = 0
pastTime = 0

#set log
detailLog = True if config.get('dbmetering_conf', 'detaillog') == 'enable' else False

#post data to Abacus
postmsg = {}
postmsg['db_storage'] = 'postgresql'
postmsg['plan_type'] = 'basic'
postmsg['measure_amount'] = 'storage'
postmsg['measure_traffic'] = 'transaction'
meteringpoint = config.get('abacus_conf', 'endpoint_' + space)

def run():
    global config, postgres_certification, duration_time
    global currentTime, pastTime
    global sql_sizes, sql_trans
    global postmsg
    currentTime = int(time.time()) * 1000
    pastTime = currentTime
    f = open('log.txt', 'a')
    log(f, str(currentTime) + ": [Info] Hello cf-service-postgresql_metering" + "\n")
    conn = psycopg2.connect(postgres_certification)
    cur = conn.cursor()
    log(f, str(currentTime) + ": [Info] postgresql certification: " + str(postgres_certification) + "\n")
    try:
        client, credentials_info = loginCF(config)
    except:
        log(f, str(currentTime) + ": [Warning] cf login failed" + "\n")
        exit(0)
    log(f, str(currentTime) + ": [Info] cf login user: " + config.get('pcf_conf', 'user') + "\n")
    log(f, str(currentTime) + ": [Info] cf login info: "+ str(credentials_info) + "\n")

    f.close()
    while True:
        cur.execute(sql_dbnames)
        dbnames = cur.fetchall()
        conn.commit()
        f = open('log.txt', 'a')
        log(f, str(currentTime) + ": [Info] abacus endpoint: "+ str(meteringpoint) + "\n")
        for i in dbnames:
            if i[0] != 'template0' and i[0] != 'template1' and i[0] != 'postgres':
                try:
                    UUID(i[0])
                except:
                    if detailLog:
                        log(f, str(currentTime) + ": [Warning] invalid dbname guid format " + i[0] + "\n")
                    continue
                currentTime = int(time.time()) * 1000
                try:
                    cur.execute(sql_size.replace('mydb', str(i[0])))
                except:
                    log(f, str(currentTime) + ": [Warning] failed to get dbsize of " + i[0] + "\n")
                    continue
                size = cur.fetchone()
                conn.commit()
                try:
                    cur.execute(sql_trans.replace('mydb', str(i[0])))
                except:
                    log(f, str(currentTime) + ": [Warning] failed to get  dbtrans of " + i[0] + "\n")
                    continue
                dbtrans = cur.fetchone()
                conn.commit()
                try:
                    service_guid, app_guid, space_guid, org_guid = getServiceInfo(client, i[0])
                except:
                    if detailLog:
                        log(f, str(currentTime) + ": [Warning] dbname " + i[0] + " call getServiceInfo failed" + "\n")
                    continue
                if service_guid == -1:
                    if detailLog:
                        log(f, str(currentTime) + ": [Warning] dbname " + i[0] + " can not be found in cf service-instances list" + "\n")
                    continue
                if app_guid == -1:
                    app_guid = '00000000-0000-0000-0000-000000000000'
                    if detailLog:
                        log(f, str(currentTime) + ": [Warning] service-instance " + i[0] + " can not find binding app" + "\n")
                postmsg['start_timestamp'] = pastTime
                postmsg['end_timestamp'] = currentTime
                postmsg['app_guid'] = str(app_guid)
                postmsg['service_guid'] = str(service_guid)
                postmsg['space_guid'] = str(space_guid)
                postmsg['org_guid'] = str(org_guid)
                postmsg['storage_size'] = str(sizeNormalize(size[0]))
                postmsg['transaction_count'] = str(dbtrans[0])
                try:
                    postResult = toAbacus(postmsg, meteringpoint)
                    metering_data = [i[0], size[0], str(dbtrans[0]), str(service_guid), str(app_guid), str(space_guid), str(org_guid), "sent metering to abacus successfully with response " + str(postResult.status_code)]
                except:
                    metering_data = [i[0], size[0], str(dbtrans[0]), str(service_guid), str(app_guid), str(space_guid), str(org_guid), "send metering to abacus failed"]

                if detailLog:
                    log(f, str(currentTime) + ": [Info] " + str(metering_data) + "\n")
        f.close()
        pastTime = currentTime
        time.sleep(duration_time)

if __name__ == "__main__":
    run()




