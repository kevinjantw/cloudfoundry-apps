# Cloud Foundry Node Red Dashboard
A node red dashboard in nodejs

## Contact
kevinjan@iii.org.tw  

## Installations & Running  
1. Install Cloud Foundry CLI  
   https://docs.cloudfoundry.org/cf-cli/install-go-cli.html

2. Cloud Foundry login from client
   ```shell= 
   cf login -a $API_DOMAIN --skip-ssl-validation -u $USER_NAME -p $USER_PASSWORD
   ```
   
3. Running  
  `Currently, api.iii-cflab.com has a nodejs dependencies issue.`  
  `Only Cloud Foundry push method (2) is working, method (1) is still not working.`  
   (1) Push node red dashboard to Cloud Foundry
   ```shell= 
    cf delete cf-nodered-dashboard -f    
   ``` 
   _Note: Remove existent app "cf-nodered-dashboard" to avoid cf push failed or change name "cf-nodered-dashboard" defined in manifest.yml_
   ```shell= 
    cf push
   ``` 
   (2) Push node red dashboard to Cloud Foundry with prefetch node module
   ```shell= 
    cf delete cf-nodered-dashboard -f
   ``` 
   ```shell= 
    npm install node-red
   ``` 
   ```shell= 
    cf push
   ``` 
4. Open node red dashboard    
   Example urls: http://cf-nodered-dashboard.iii-cflab.com
   ```shell= 
    ###############################################################################
    requested state: started
    instances: 1/1
    usage: 1G x 1 instances
    urls: cf-nodered-dashboard.iii-cflab.com
    last uploaded: Fri Nov 24 09:17:25 UTC 2017
    stack: cflinuxfs2
    buildpack: https://github.com/cloudfoundry/nodejs-buildpack.git

    state     since                    cpu    memory        disk           details
    running   2017-11-24 05:18:50 PM   0.0%   81.8M of 1G   119.5M of 1G
    ###############################################################################
   ```