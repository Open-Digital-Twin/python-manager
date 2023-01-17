from api import call_scale_cluster

def scale_cluster (max_inflight, max_queue, avg_inflight, avg_queue):

    print("avg inflight is " + str(avg_inflight) + " (max) " + str(max_inflight))
    print("avg queue is " + str(avg_queue) + " (max) " + str(max_queue))
    if(max_inflight < avg_inflight and max_queue < avg_queue):
        call_scale_cluster("address")
