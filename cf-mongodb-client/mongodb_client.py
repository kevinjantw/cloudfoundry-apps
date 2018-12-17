import os, json
import pymongo
from pymongo import MongoClient

# Hello
print "Hello pymongo"

# Get mongo uri
vcap_services = json.loads(os.getenv('VCAP_SERVICES'))
uri = vcap_services.values()[0][0]['credentials']['uri']
print "pymongo uri:",uri

# Connect to mongo
client = MongoClient(uri)
print 'pymongo connection:', str(client)

# Switch to default mongo db
test = {'org':'iii', 'event': 'demo'}
db = client.get_default_database()

# Insert test data to default db with event collection 
result = db.event.insert_one(test)
print 'pymongo insert test_id:', result.inserted_id 

# Find data {'org':iii} from default db with event collection
print 'pymongo find result:', db.event.find_one({'org':'iii'})

client.close()
