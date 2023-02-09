from kubernetes import client, config
import time


def check_params (response_client, response_nodes, max_queue, max_inflight):
    total_queue = 0
    metrics = response_client.json()
    nodes = response_nodes.json()
    for i in range(len(metrics["data"])):
        print ("Client " + str(metrics["data"][i]["clientid"]) + " Queue : " + str(metrics["data"][i]["mqueue_len"]))
        total_queue = total_queue + metrics["data"][i]["mqueue_len"]
    print("Current nodes: " + str(len(nodes)))
    print("Current queue: " + str(total_queue))
    if (total_queue/len(nodes) > int(max_queue)):
        print("Returning scale = True")
        return True
    return False


def scale_cluster(kube_client):
        name = 'emqx'
        namespace = 'dtwins'
        emqx_body = kube_client.read_namespaced_stateful_set(name, namespace)
        if emqx_body.spec.replicas < 3 :
            emqx_body.spec.replicas = emqx_body.spec.replicas + 1
            body = emqx_body
            api_response = kube_client.patch_namespaced_stateful_set_scale(name, namespace, body)
            print("Scaling cluster...")
            time.sleep(30);
        else :
            print("Maximum cluster size achieved")
            time.sleep(10)