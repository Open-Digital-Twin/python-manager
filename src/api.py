import requests
import json

def call_api_cluster(address,port):
    params = {
        "aggregate" : "true"
    }
    response = requests.get("http://" + address + ":" + port +"/api/v5/metrics", params=params, auth=('admin','public'))
    return response

def call_api_nodes(address, port):
    response = requests.get("http://" + address + ":" + port + "/api/v5/nodes", auth=('admin','public'))
    return response