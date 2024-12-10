import time
import os
from api import call_api_clients, call_api_nodes
from scale_logic import check_params, scale_cluster
from kubernetes import client, config

def main():

    cluster_address = os.getenv("API_ADDRESS_CLUSTER")
    cluster_port = os.getenv("CLUSTER_PORT")
    cluster_user = os.getenv("CLUSTER_USER")
    cluster_password = os.getenv("CLUSTER_PASSWORD")
    kube_address = os.getenv("API_ADDRESS_KUBE")
    kube_port= os.getenv("KUBE_PORT")
    api_interval = os.getenv("API_INTERVAL")
    max_queue = os.getenv("MAX_QUEUE")
    max_inflight = os.getenv("MAX_INFLIGHT")
    method = os.getenv("METHOD")

    
    config.load_incluster_config()
    kube_client = client.AppsV1Api()

    print("starting with cluster address: " + cluster_address + ":" + cluster_port)
    print("cluster user set to: " + cluster_user + " and cluster password set to: " + cluster_password)
    print("kubernetes api address set to: " + kube_address + ":" + kube_port)
    print("max queue set to: " + max_queue + " and max inflight set to: " + max_inflight)


    while(True):
        response_clients = call_api_clients(cluster_address,cluster_port, cluster_user, cluster_password)
        response_nodes = call_api_nodes(cluster_address,cluster_port, cluster_user, cluster_password)

        if (response_clients.status_code == 200 and response_nodes.status_code == 200):
            #print("Data received :" + str(response_clients.json()["data"]))
            #print("Additional clients" + str(response_nodes.json()[0]))
            if  check_params(response_clients,response_nodes, max_queue, max_inflight, method):
                scale_cluster(kube_client)
            time.sleep(int(api_interval))

        else:
            print("error in api request " + str((response_clients.status_code)) + " "  + str(response_nodes.status_code))
            time.sleep(int(api_interval))

if __name__ == "__main__" :
    main()