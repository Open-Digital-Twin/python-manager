from kubernetes import client, config


def check_params (response_metric, response_nodes, max_queue, max_inflight):
    metrics = response_metric.json()
    print("current queue: " + str(metrics['messages.qos1.received'] - metrics['messages.qos1.sent'])) 
    if (metrics['messages.qos1.received'] - metrics['messages.qos1.sent']) > int(max_queue):
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