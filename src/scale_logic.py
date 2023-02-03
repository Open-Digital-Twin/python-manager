from kubernetes import client, config


def check_params (response_clients, response_nodes, max_queue, max_inflight):
    total_queue = 0
    metrics = response_clients.json()
    for i in range(len(metrics["data"])):
        print("Data received :" + str(response_clients.json()["data"][i]["mqueue_len"]))
        #total_queue = total_queue + metrics[i]["mqueue_len"]

    print("current queue: " + str(total_queue)) 
    if total_queue > int(max_queue):
        return True
    return False


def scale_cluster(kube_client):
        name = 'emqx'
        namespace = 'dtwins'
        emqx_body = kube_client.read_namespaced_stateful_set(name, namespace)
        print(emqx_body.spec.replicas)
        emqx_body.spec.replicas = emqx_body.spec.replicas + 1
        body = emqx_body
        api_response = kube_client.patch_namespaced_stateful_set_scale(name, namespace, body)