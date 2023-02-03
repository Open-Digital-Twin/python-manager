import requests

#def call_api_metrics(address,port):
#    params = {
#        "aggregate" : "true"
#    }
#    response = requests.get("http://" + address + ":" + port +"/api/v5/metrics", params=params, auth=('admin','public'))
#    return response

def call_api_nodes(address, port):
    response = requests.get("http://" + address + ":" + port + "/api/v5/nodes", auth=("admin","public"))
    return response

def call_api_clients(address, port):
    response = requests.get("http://" + address + ":" + port + "/api/v5/clients", auth=("admin","public"))
    return response