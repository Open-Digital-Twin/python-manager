import requests
import json

def call_api_cluster(address,port):
    print("calling http://" + address + ":" + port +"/api/v5/clients")
    response = requests.get("http://" + address + ":" + port +"/api/v5/clients")
    return response

def call_api_nodes(address, port):
    print("calling http://" + address + ":" + port + "/api/v5/nodes")
    response = requests.get("http://" + address + ":" + port + "/api/v5/nodes")
    return response

def call_scale_cluster(address,port):
    print("TODO")