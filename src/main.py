import time
import os
from api import call_api_cluster, call_api_nodes
from scale_logic import check_params, scale_cluster
from kubernetes import client, config

def main():

    cluster_address = os.getenv("API_ADDRESS_CLUSTER")
    cluster_port = os.getenv("CLUSTER_PORT")
    kube_address = os.getenv("API_ADDRESS_KUBE")
    kube_port= os.getenv("KUBE_PORT")
    api_interval = os.getenv("API_INTERVAL")
    max_queue = os.getenv("MAX_QUEUE")
    max_inflight = os.getenv("MAX_INFLIGHT")
    
    config.load_incluster_config()
    kube_client = client.CoreV1Api()

    print("starting with cluster address: " + cluster_address + ":" + cluster_port)
    print("kubernetes api address set to: " + kube_address + ":" + kube_port)
    print("max queue set to: " + max_queue + " and max inflight set to: " + max_inflight)

    while(True):
        response_clients = call_api_cluster(cluster_address,cluster_port)
        response_nodes = call_api_nodes(cluster_address,cluster_port)

        if (response_clients.status_code == 200 and response_nodes.status_code == 200):
            #print("Data received :" + str(response_clients.json()["data"]))
            #print("Additional metrics" + str(response_nodes.json()[0]))
            
            #check_params(int(max_inflight), int(max_queue) , avg_inflight , avg_queue)
            scale_cluster(kube_client)
            time.sleep(5)

        else:
            #print("error in api request " + str((response_cluster.status_code)) + " "  + str(response_nodes.status_code))
            #print("its alive")
            time.sleep(5)

if __name__ == "__main__" :
    main()