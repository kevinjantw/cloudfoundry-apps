# -*- coding: utf8 -*-
import os, sys, time
import json, ast
import requests
import threading
from flask import Flask
from flask import request

lock = threading.Lock()
fireHoseData = {}
featureData = {}
matchCount = 0
headers = {'Content-type': 'application/json'}
classifier_api = "http://motor-classifier-c.iii-cflab.com/motorclassifier-c"

def add2fireHoseData(content):
    global matchCount
    match = ""
    if "Machine_ID" in content and "Time" in content:
        id = str(content["Machine_ID"])
        time_stamp = str(content["Time"])
        id_time_stamp = id + "_" + time_stamp
        lock.acquire()
        if id_time_stamp in featureData:
            print "JSON Has Matching Key: ", id_time_stamp
            match = featureData[id_time_stamp]
            matchCount += 1
            featureData.pop(id_time_stamp)
        else:
            fireHoseData.update({id_time_stamp: content})
        lock.release()
    return match

def add2featureData(content):
    global matchCount
    match = ""
    if "Machine_ID" in content and "Time" in content:
        id = str(content["Machine_ID"])
        time_stamp = str(content["Time"])
        id_time_stamp = id + "_" + time_stamp
        lock.acquire()
        if id_time_stamp in fireHoseData:
            print "JSON Has Matching Key: ", id_time_stamp
            match = fireHoseData[id_time_stamp]
            matchCount += 1
            fireHoseData.pop(id_time_stamp)
        else:
            featureData.update({id_time_stamp: content})
        lock.release()
    return match

app = Flask(__name__)

@app.route('/firehose_post', methods = ['POST'])
def fireHoseHandler():
    if not request.is_json:
        return "Invalid JSON Content"
    content = request.get_json()
    print "JSON Content is: ", str(content)
    match_result = add2fireHoseData(content)
    if match_result != "":
        response_json = {"firehoseData":content, "featureData":match_result}
        r = requests.post(classifier_api, headers=headers, json=response_json)
        print "Classifier Response: ", str(r.status_code)
        print "Classifier Response Content: ", str(r.text)
        return str(ast.literal_eval(json.dumps(response_json)))
    else:
        return "JSON Posted with no matching"

@app.route('/feature_post', methods = ['POST'])
def featureHandler():
    if not request.is_json:
        return "Invalid JSON Content"
    content = request.get_json()
    print "JSON Content is: ", str(content)
    match_result = add2featureData(content)
    if match_result != "":
        response_json = {"firehoseData":match_result, "featureData":content}
        r = requests.post(classifier_api, headers=headers, json=response_json)
        print "Classifier Response: ", str(r.status_code)
        print "Classifier Response Content: ", str(r.text)
        return str(ast.literal_eval(json.dumps(response_json)))
    else:
        return "JSON Posted with no matching"

@app.route('/get_data')
def get_data():
    global matchCount
    return "[Hello JSON Matching] " + \
           "matchCount: " + str(matchCount) + \
           ", " + "fireHoseData: " + str(fireHoseData) + \
           ", " + "featureData: " + str(featureData)

port = os.getenv('PORT', '8080')
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = int(port))
    
