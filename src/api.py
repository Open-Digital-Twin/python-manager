import requests
import os
def call_api_clients(address,port, cluster_user, cluster_password):
    params = {
        "like_clientid" : "sub"
    }

    response = requests.get("http://" + address + ":" + port + "/api/v5/clients", params=params, auth=(cluster_user,cluster_password))
    return response

def call_api_nodes(address, port, cluster_user, cluster_password):

    response = requests.get("http://" + address + ":" + port + "/api/v5/nodes", auth=(cluster_user,cluster_password))
    return response