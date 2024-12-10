from kubernetes import client, config
import time
from datetime import datetime

def check_params(response_client, response_nodes, max_queue, max_inflight, method): 
    metrics = response_client.json()
    nodes = response_nodes.json()
    
    # Calculate both metrics
    queue_total = sum(metric["mqueue_len"] for metric in metrics["data"])
    inflight_total = sum(metric["inflight_cnt"] for metric in metrics["data"])
    node_count = len(nodes)
    
    # Print both metrics
    print(f"date: {datetime.now()} | Queue: total={queue_total}, avg={queue_total/node_count:.2f}, max={max_queue} | Inflight: total={inflight_total}, avg={inflight_total/node_count:.2f}, max={max_inflight}")
    
    # Make scaling decision based on specified method
    if method == "queue":
        should_scale = queue_total/node_count > int(max_queue)
    else:
        should_scale = inflight_total/node_count > int(max_inflight)
    
    if should_scale:
        print(f"Returning scale = True ({method} threshold exceeded)")
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
            print(api_response)
            time.sleep(30);
        else :
            print("Maximum cluster size achieved")
            time.sleep(10)