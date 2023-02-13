import requests

def call_api_clients(address,port):
    params = {
        "like_clientid" : "twin"
    }
    response = requests.get("http://" + address + ":" + port + "/api/v5/clients", params=params, auth=('admin','public'))
    return response

def call_api_nodes(address, port):
    response = requests.get("http://" + address + ":" + port + "/api/v5/nodes", auth=("admin","public"))
    return response