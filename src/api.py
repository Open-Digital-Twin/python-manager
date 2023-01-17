import requests
import json

def call_api_cluster(address):
    response = requests.get("http://" + url + "/api/v5/clients")
    return response

def call_api_nodes(address):
    response = requests.get("http://" + url + "/api/v5/nodes")
    return response

def call_scale_cluster(address):
    print("TODO")