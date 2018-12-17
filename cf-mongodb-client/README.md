# Cloud Foundry Mongodb Client
A mongodb client example in pymongo

## Contact
kevinjan@iii.org.tw  

## Installations & Running  
1. Install Cloud Foundry CLI  
   https://docs.cloudfoundry.org/cf-cli/install-go-cli.html

2. Cloud Foundry login from client
   ```shell= 
   cf login -a $API_DOMAIN --skip-ssl-validation -u $USER_NAME -p $USER_PASSWORD
   ```
   
3. Run mongodb client example on Cloud Foundry  
   (1) List Cloud Foundry services from marketplace
   ```shell= 
    cf marketplace
   ``` 
   ```shell= 
    ##############################################################################################################################################
    Getting services from marketplace in org WISE-PaaS / space Develop as admin...
    OK
    service                           plans                    description
    app-autoscaler                    standard                 Scales bound applications in response to load (beta)
    mongodb-wise-paas-develop         Free-Tier, Paid2-Tier*   A simple MongoDB service broker implementation
    mongodb-wise-paas-production      Free-Tier                A simple MongoDB service broker implementation
    mongodb-wise-paas-stage           Free-Tier, Paid2-Tier*   A simple MongoDB service broker implementation
    p-rabbitmq                        standard                 RabbitMQ is a robust and scalable high-performance multi-protocol messaging broker.
    p.rabbitmq                        solo                     RabbitMQ Service
    postgresql-wise-paas-develop      Free-Tier*, Paid2-Tier   PostgreSQL on shared instance.
    postgresql-wise-paas-production   Free-Tier                PostgreSQL on shared instance.
    postgresql-wise-paas-stage        Free-Tier                PostgreSQL on shared instance.
    ##############################################################################################################################################
   ```
   (2) Create a service instance "mongodb-service-demo" from service "mongodb-wise-paas-develop" with plan 'Free-Tier'
   ```shell= 
    cf create-service mongodb-wise-paas-develop 'Free-Tier' mongodb-service-demo
   ``` 
   ```shell= 
    ##############################################################################################################################################
    Creating service instance mongodb-service-demo in org WISE-PaaS / space Develop as admin...
    OK
    ##############################################################################################################################################
   ```
   (3) Push mongodb client app to Cloud Foundry without running
   ```shell= 
    cf push --no-start
   ``` 
   ```shell= 
    ##############################################################################################################################################
    Using manifest file /home/kevinjan/cf-mongodb/manifest.yml
    Creating app mongodb_client in org WISE-PaaS / space Develop as admin...
    OK
    App mongodb_client is a worker, skipping route creation
    Uploading mongodb_client...
    Uploading app files from: /home/kevinjan/cf-mongodb
    Uploading 820B, 3 files
    Done uploading
    OK
    ##############################################################################################################################################
   ```
   (4) Bind service instance "mongodb-service-demo" to mongodb client app
   ```shell= 
    cf bind-service mongodb_client mongodb-service-demo
   ``` 
   ```shell= 
    ##############################################################################################################################################
    Binding service mongodb-service-demo to app mongodb_client in org WISE-PaaS / space Develop as admin...
    OK
    ##############################################################################################################################################
   ```
   (5) View binded environment variables in mongodb client app
   ```shell= 
    cf env mongodb_client
   ``` 
   ```shell= 
    ##############################################################################################################################################
    System-Provided:
    {"VCAP_SERVICES": { xxx, "uri": "mongodb://xxx", ... }}  {"VCAP_APPLICATION": { xxx, ... }} 
    ##############################################################################################################################################
   ```
   (6) Run mongodb client app
   ```shell= 
    cf start mongodb_client
   ```
   ```shell= 
    ##############################################################################################################################################
    name:              mongodb_client
    requested state:   started
    instances:         1/1
    usage:             512M x 1 instances
    routes:
    last uploaded:     Fri 24 Nov 13:55:53 CST 2017
    stack:             cflinuxfs2
    buildpack:         python_buildpack
    start command:     python mongodb_client.py
    
    state     since                  cpu    memory      disk      details
    running   2017-11-24T06:08:43Z   0.0%   0 of 512M   0 of 1G
    ##############################################################################################################################################
   ```
   (7) View recent logs of mongodb client app
   ```shell= 
    cf logs mongodb_client --recent
   ```
   ```shell= 
    ########################################################################################################################################################################################################################################################################################################################################################################
    2017-11-24T14:08:42.20+0800 [CELL/0] OUT Creating container
    2017-11-24T14:08:43.30+0800 [STG/0] OUT Successfully destroyed container
    2017-11-24T14:08:43.84+0800 [CELL/0] OUT Successfully created container
    2017-11-24T14:08:46.92+0800 [APP/PROC/WEB/0] OUT Hello pymongo
    2017-11-24T14:08:46.92+0800 [APP/PROC/WEB/0] OUT pymongo uri: mongodb://5c248add-d78b-4277-aa99-a220256ddecf:A25zBgazcaL7lv5Pk1S5p0QUo@192.168.0.14:27017,192.168.0.15:27017,192.168.0.15:27018/79817b79-9a15-46de-9628-3544cb0cfc84
    2017-11-24T14:08:46.93+0800 [APP/PROC/WEB/0] OUT pymongo connection: MongoClient(host=[u'192.168.0.14:27017', u'192.168.0.15:27018', u'192.168.0.15:27017'], document_class=dict, tz_aware=False, connect=True)
    2017-11-24T14:08:47.08+0800 [APP/PROC/WEB/0] OUT pymongo insert test_id: 5a17b76e7f5e5b0013f0a904
    2017-11-24T14:08:47.08+0800 [APP/PROC/WEB/0] OUT pymongo find result: {u'org': u'iii', u'_id': ObjectId('5a17b76e7f5e5b0013f0a904'), u'event': u'demo'}
    2017-11-24T14:08:47.46+0800 [APP/PROC/WEB/0] OUT Exit status 0
    2017-11-24T14:08:47.46+0800 [CELL/0] OUT Exit status 0
    2017-11-24T14:08:47.49+0800 [CELL/0] OUT Destroying container
    2017-11-24T14:08:47.51+0800 [API/0] OUT Process has crashed with type: "web"
    2017-11-24T14:08:47.52+0800 [API/0] OUT App instance exited with guid b1572512-55ec-4ee9-85d1-f002b713b949 payload: {"instance"=>"", "index"=>0, "reason"=>"CRASHED", "exit_description"=>"2 error(s) occurred:\n\n* Codependent step exited\n* cancelled", "crash_count"=>1, "crash_timestamp"=>1511503727466297039, "version"=>"9a9905c6-7331-4756-9275-86b2f7b50d1e"}
    ########################################################################################################################################################################################################################################################################################################################################################################
   ```