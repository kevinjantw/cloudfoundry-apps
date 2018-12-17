# Cloud Foundry JSON Posts Matching
A JSON posts matching in Flask RestFul APIs

## Contact
kevinjan@iii.org.tw  

## Installations & Running  
1. Install Cloud Foundry CLI  
   https://docs.cloudfoundry.org/cf-cli/install-go-cli.html

2. Cloud Foundry login from client
   ```shell= 
   cf login -a $DOMAIN.COM --skip-ssl-validation -u $USER_NAME -p $USER_PASSWORD
   ```
   
3. Run JSON posts matching on Cloud Foundry
   ```shell= 
    cf delete cf-json-matching -f    
   ```
   _Note: Remove existent app "cf-json-matching" to avoid cf push failed or change name "cf-json-matching" defined in manifest.yml_
   ```shell= 
    cf push
   ```   
4. RestFul APIs from client
   ```shell= 
    URI: http://cf-json-matching.iii-cflab.com/firehose_post
    Method: POST
    Headers: {'Content-type': 'application/json'}
    Body:
    {
		"Machine_ID": "001",
		"V1": [20, 20, 20, 20],
		"V2": [20, 20, 20, 20],
		"V3": [20, 20, 20, 20],
		"I1": [20, 20, 20, 20],
		"I2": [20, 20, 20, 20],
		"I3": [20, 20, 20, 20],
		"A1": [20, 20, 20, 20],
		"A2": [20, 20, 20, 20],
		"A3": [20, 20, 20, 20],
		"Time": 1511425672
	}
   ``` 
   ```shell= 
    http://cf-json-matching.iii-cflab.com/feature_post
    Method: POST
    Headers: {'Content-type': 'application/json'}
    Body:
    {
		"Machine_ID": "001",
		"list_V1": [30, 30, 30, 30],
		"list_V2": [30, 30, 30, 30],
		"list_V3": [30, 30, 30, 30],
		"list_I1": [30, 30, 30, 30],
		"list_I2": [30, 30, 30, 30],
		"list_I3": [30, 30, 30, 30],
		"Time": 1511425672
	}
   ``` 
   ```shell= 
    http://cf-json-matching.iii-cflab.com/get_data
    Method: GET
    Response: 
    [Hello JSON Matching] matchCount: 0, fireHoseData: {}, featureData:{}
   ``` 
   _Note: "cf-json-matching" is a host defined in manifest.yml and "iii-cflab.com" depends on cf login $DOMAIN.COM_
   
5. Pass matching data to Motor-classifier  
   ```shell= 
    URI: http://motor-classifier-c.iii-cflab.com/motorclassifier-c
    Method: POST
    Headers: {'Content-type': 'application/json'}
    Body:
    {
		"firehoseData": {
		"Machine_ID": "001",
		"V1": [20, 20, 20, 20],
		"V2": [20, 20, 20, 20],
		"V3": [20, 20, 20, 20],
		"I1": [20, 20, 20, 20],
		"I2": [20, 20, 20, 20],
		"I3": [20, 20, 20, 20],
		"A1": [20, 20, 20, 20],
		"A2": [20, 20, 20, 20],
		"A3": [20, 20, 20, 20],
		"Time": 1511425672
	    },
	    "featureData": {
		"Machine_ID": "001",
		"list_V1": [30, 30, 30, 30],
		"list_V2": [30, 30, 30, 30],
		"list_V3": [30, 30, 30, 30],
		"list_I1": [30, 30, 30, 30],
		"list_I2": [30, 30, 30, 30],
		"list_I3": [30, 30, 30, 30],
		"Time": 1511425672
	    }
	}
   ```
6. RestFul APIs test tool  
   http://www.getpostman.com/