from kubernetes import client, config


def check_params (max_inflight, max_queue, avg_inflight, avg_queue):

    print("avg inflight is " + str(avg_inflight) + " (max) " + str(max_inflight))
    print("avg queue is " + str(avg_queue) + " (max) " + str(max_queue))
    if(max_inflight < avg_inflight and max_queue < avg_queue):
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