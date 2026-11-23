import requests
import time
import json
import pprint
import threading
#import numpy as np
#from matplotlib import mlab
#import matplotlib.pyplot as plt

latency_arr = []
latency_arr_overall = []

def latency_test(latency):
    global latency_arr
    print("==============================50 ms LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection

    # INJECT TOXIC
    i = 1
    while (i < 51):

        # TODO fix toxic injection for consul2 and consul3
        # TODO fix why latencies are not causing leader elections
        payload = {
            "name": f"latency_{i}",
            "type": "latency",
            "stream": "upstream",
            "attributes": {"latency": i*latency, "jitter": 0} # i.e. increasing latency by 50 ms after each loop
        }

        # inject toxics
        requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
        requests.post(f"http://localhost:8475/proxies/consul2/toxics", json=payload)
        requests.post(f"http://localhost:8476/proxies/consul3/toxics", json=payload)
        #print(f"Total latency injected: {i*500}. Waiting ...")

#         payload = {
#             "name": f"latency_1_{i}",
#             "type": "latency",
#             "stream": "downstream",
#             "attributes": {"latency": i*latency, "jitter": 0} # i.e. increasing latency by 50 ms after each loop
#         }
#
#         requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
#         requests.post(f"http://localhost:8475/proxies/consul2/toxics", json=payload)
#         requests.post(f"http://localhost:8476/proxies/consul3/toxics", json=payload)

        # verify toxics were created
        json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
        print(json_data.json())
        time.sleep(5)
        json_data = requests.get(f"http://localhost:8475/proxies/consul2/toxics")
        print(json_data.json())
        time.sleep(5)
        json_data = requests.get(f"http://localhost:8476/proxies/consul3/toxics")
        print(json_data.json())
        t1 = threading.Thread(get_metrics(), args=())
        t1.start()
        #time.sleep(240)
        t1.join()

        # clean up
        requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_{i}")
        requests.delete(f"http://localhost:8475/proxies/consul2/toxics/latency_{i}")
        requests.delete(f"http://localhost:8476/proxies/consul3/toxics/latency_{i}")
#         requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_1_{i}")
#         requests.delete(f"http://localhost:8475/proxies/consul2/toxics/latency_1_{i}")
#         requests.delete(f"http://localhost:8476/proxies/consul3/toxics/latency_1_{i}")

        i += 1

def plot_percentiles(figure_num, file_name):
    global latency_arr

    arr = np.array(latency_arr)
    arr.sort()
    p = np.array([0.0, 50.0, 99.0])

    perc = np.percentile(arr, p)

    plt.figure(figure_num)
    plt.plot(arr)
    plt.plot((len(arr)-1)*p/100., perc, 'ro')
    plt.xticks((len(arr)-1)*p/100., map(str, p))

    plt.savefig(file_name)

def get_metrics():
    TOXIPROXY_API = "http://localhost:8500" # metrics
    # pretty print dictionary
    pp = pprint.PrettyPrinter(indent=1, width=20)
    i = 0
    while (i < 10):
        json_data = requests.get(f"{TOXIPROXY_API}/v1/status/leader")
    #json_data = requests.get(f"{TOXIPROXY_API}/v1/agent/metrics")

        pp.pprint(json_data.json())
        time.sleep(10)
        i += 1
    #print(json_data.json())

def main():
    global latency_arr
    latency_test(3500)

main()




# TOXIPROXY_API = "http://localhost:8500" # metrics
# # pretty print dictionary
# pp = pprint.PrettyPrinter(indent=1, width=20)
#
# # GET METRICS: Cluster stability
# json_data = requests.get(f"{TOXIPROXY_API}/v1/agent/metrics")
# pp.pprint(json_data.json())
#
# # GET CONFIGURATION: Track state divergence
# json_data = requests.get(f"{TOXIPROXY_API}/v1/operator/raft/configuration")
# pp.pprint(json_data.json())