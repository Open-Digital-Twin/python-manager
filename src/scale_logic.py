from kubernetes import client, config
import time


def check_params (response_metric, response_nodes, max_queue, max_inflight):
    metrics = response_metric.json()
    nodes = response_nodes.json()
    print("current queue : " + str(metrics['messages.qos1.received'] - (metrics['messages.qos1.sent'] - metrics['messages.dropped'])))
    print("average queue : " + str((metrics['messages.qos1.received'] - (metrics['messages.qos1.sent'] - metrics['messages.dropped']))/len(nodes)))
    print("cluster current size: " + str(len(nodes))) 
    if (metrics['messages.qos1.received'] - (metrics['messages.qos1.sent']+ metrics['messages.dropped'])/len(nodes) > int(max_queue)):
        print("returning scale = True")
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
            print("scaling cluster...")
            time.sleep(30);
        else :
            print("maximum cluster size achieved")
            time.sleep(30)