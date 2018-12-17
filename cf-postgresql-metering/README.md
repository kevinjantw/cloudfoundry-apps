# Cloud Foundry PostgreSQL DB Metering  
Metering postgresql transaction count and dbsize

## Contact  
kevinjan@iii.org.tw  

## Release Notes  
1. Version 1.0.1  
2. Configurable postgresql metering duration time in second  
3. Support postgresql metering agent messages to log  
4. A postgresql metering deploy & run script on Cloud Foundry app  

## Installations & Running  
1. All postgresql metering functionalities only tested under   
(a) ubuntu 14.04  
(b) posstgresql 9.6.2  
(c) python 2.7

2. Before running, configure your env variables in configs.ini   
(a) Configure postgresql metering duration time in second  
(b) "enable" or "disable" detaillog ("disable" for minimal log size)   
(c) Set postgresql admin/password/dbname/host/port  
(d) Set pcf endpoint/user(admin)/password  
(e) Set abacus metering endpoint  
   
3. Install and run postgresql metering on locally   
(a) Install psycopg2  
    ```shell= 
    sudo apt-get install python-pip
    ```
    ```shell= 
    sudo apt-get install python-dev libpq-dev 
    ```
    ```shell= 
    pip install psycopg2
    ```
(b) Install Cloud Foundry CLI  
    ```shell= 
    pip install cloudfoundry_client
    ```   
(c) Postgresql metering agent start
    ```shell= 
    python dbmetering.py
    ```    
           
4. Deploy and run postgresql metering on Cloud Foundry app
    ```shell=
    python deploy.py $space $version
    ```    
    ```shell=
    example: python deploy.py production 1.0.1
    ```

5. Deploy and run postgresql metering via Jenkins  
   (a) Configure default parameters in "Build with parameters"  
   (b) Click "Start to build"  
    
6. Run unit tests  
   (a) Configure your env variables in configs.ini  
   (b) Run tests  
    ```shell=
    python unittests.py
    ```
