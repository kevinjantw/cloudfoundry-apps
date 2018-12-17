# Cloud Foundry Node Hello
A "Hello World" nodejs example for Cloud Foundry

## Contact
kevinjan@iii.org.tw  

## Original Source
https://github.com/pmuellr/cf-node-hello

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
   (1) Push nodejs example to Cloud Foundry
   ```shell= 
    cf delete cf-node-hello -f    
   ``` 
   _Note: Remove existent app "cf-node-hello" to avoid cf push failed or change name "cf-node-hello" defined in manifest.yml_
   ```shell= 
    cf push
   ``` 
   (2) Push nodejs example to Cloud Foundry with prefetch node modules
   ```shell= 
    cf delete cf-node-hello -f    
   ``` 
   ```shell= 
    npm install cfenv
   ``` 
   ```shell= 
    cf push
   ``` 
   (3) Run nodejs example on locally 
   ```shell= 
   npm install cfenv
   ``` 
   ```shell= 
   node server.js
   ``` 


