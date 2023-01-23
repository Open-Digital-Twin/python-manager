import requests
import json

def call_api_cluster(address,port):
    print("calling http://" + address + ":" + port +"/api/v5/clients")
    response = requests.get("http://" + address + ":" + port +"/api/v5/clients", auth=('admin','public'))
    return response

def call_api_nodes(address, port):
    print("calling http://" + address + ":" + port + "/api/v5/nodes")
    response = requests.get("http://" + address + ":" + port + "/api/v5/nodes", auth=('admin','public'))
    return response