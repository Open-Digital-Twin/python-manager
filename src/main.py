import time
import os
from api import call_api_clients, call_api_nodes
from scale_logic import check_params, scale_cluster, descale_cluster
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
    max_size = os.getenv("MAX_SIZE")
    descale_threshold = os.getenv("DESCALE_THRESHOLD")
    descale_param = os.getenv("DESCALE_PARAM") #inflight_cnt or mqueue_lenght
    method = os.getenv("METHOD")

    no_scale = 0

    config.load_incluster_config()
    kube_client = client.AppsV1Api()

    print("starting up version 1.6")
    print("starting with cluster address: " + cluster_address + ":" + cluster_port)
    print("cluster user set to: " + cluster_user + " and cluster password set to: " + cluster_password)
    print("kubernetes api address set to: " + kube_address + ":" + kube_port)
    print("max queue set to: " + max_queue + " and max inflight set to: " + max_inflight)
    print("descale param set to: " + descale_param)


    while(True):
        response_clients = call_api_clients(cluster_address,cluster_port, cluster_user, cluster_password)
        response_nodes = call_api_nodes(cluster_address,cluster_port, cluster_user, cluster_password)
        metrics = response_clients.json()

        if (response_clients.status_code == 200 and response_nodes.status_code == 200):
            #print("Data received :" + str(response_clients.json()["data"]))
            #print("Additional clients" + str(response_nodes.json()[0]))
            if  check_params(response_clients,response_nodes, max_queue, max_inflight, method):
                scale_cluster(kube_client, max_size)
                no_scale = 0

            if sum(metric.get(descale_param, 0) for metric in metrics["data"]) == 0:
                no_scale = no_scale + 1
                print("No scale value:  " + str(no_scale))
            else :
                no_scale = 0

            if no_scale > int(descale_threshold):
                descale_cluster(kube_client)
                no_scale = 0
            time.sleep(int(api_interval))

        else:
            print("error in api request " + str((response_clients.status_code)) + " "  + str(response_nodes.status_code))
            time.sleep(int(api_interval))

if __name__ == "__main__" :
    main()