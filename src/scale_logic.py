from kubernetes import client, config
import time
from datetime import datetime

def check_params(response_client, response_nodes, max_queue, max_inflight, method):
    try:
        metrics = response_client.json()
        nodes = response_nodes.json()
        
        # Guard against empty or invalid responses
        if not metrics.get("data") or not nodes:
            print(f"Warning: Received empty or invalid response - metrics: {bool(metrics.get('data'))}, nodes: {bool(nodes)}")
            return False
        
        # Calculate both metrics with safety checks
        queue_total = sum(metric.get("mqueue_len", 0) for metric in metrics["data"])
        inflight_total = sum(metric.get("inflight_cnt", 0) for metric in metrics["data"])
        node_count = len(nodes)
        
        if node_count == 0:  # Prevent division by zero
            print("Warning: No nodes found in cluster")
            return False
            
        # Print both metrics
        print(f"date: {datetime.now()} |Cluster size: {node_count} |Queue: total={queue_total}, avg={queue_total/node_count:.2f}, max={max_queue} | Inflight: total={inflight_total}, avg={inflight_total/node_count:.2f}, max={max_inflight}")
        
        # Make scaling decision based on specified method
        if method == "queue":
            should_scale = queue_total/node_count > int(max_queue)
        else:
            should_scale = inflight_total/node_count > int(max_inflight)
        
        if should_scale:
            print(f"Returning scale = True ({method} threshold exceeded)")
            return True
        return False
        
    except (ValueError, KeyError, AttributeError) as e:
        print(f"Error processing metrics: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error in check_params: {str(e)}")
        return False

def scale_cluster(kube_client, max_size):
    try:
        name = 'emqx'
        namespace = 'dtwins'
        
        # Add retry logic for kubernetes operations
        max_retries = 3
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                emqx_body = kube_client.read_namespaced_stateful_set(name, namespace)
                
                if emqx_body.spec.replicas < int(max_size):
                    emqx_body.spec.replicas += 1
                    api_response = kube_client.patch_namespaced_stateful_set_scale(
                        name, namespace, emqx_body
                    )
                    print(f"Scaling cluster... Current replicas: {emqx_body.spec.replicas}")
                    time.sleep(30)
                    return True
                else:
                    print("Maximum cluster size achieved")
                    time.sleep(10)
                    return False
                    
            except client.rest.ApiException as e:
                if attempt < max_retries - 1:  # don't sleep on last attempt
                    print(f"Kubernetes API error (attempt {attempt + 1}/{max_retries}): {e}")
                    time.sleep(retry_delay)
                else:
                    raise  # re-raise on final attempt
                    
    except client.rest.ApiException as e:
        print(f"Kubernetes API error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in scale_cluster: {str(e)}")
        return False