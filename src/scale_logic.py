from kubernetes import client, config


def check_params (max_inflight, max_queue, avg_inflight, avg_queue):
    print("avg inflight is " + str(avg_inflight) + " (max) " + str(max_inflight))
    print("avg queue is " + str(avg_queue) + " (max) " + str(max_queue))
    if(max_inflight < avg_inflight and max_queue < avg_queue):
        call_scale_cluster("address")


def scale_cluster(kube_client):
    service_list = kube_client.list_namespaced_service("dtwins")
    print(service_list)