import requests
import time
import json
import pprint
import numpy as np

latency_arr = []

def writes():
    global latency_arr
    TOXIPROXY_API = "http://localhost:8500" # metrics
    payload = {
        "my-key": 2,
    }
    i = 0
    while (i < 50):
        #print(requests.get(f"{TOXIPROXY_API}/v1/kv/my-key"))
        before_time = time.time()
        print(requests.put(f"{TOXIPROXY_API}/v1/kv/my-key", json=payload))
        after_time = time.time()
        latency = (after_time - before_time)
        latency_arr.append(latency)
        i += 1

def five_percent_latency():
    print("==============================5% LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_5",
        "type": "latency",
        "attributes": {"latency": 5000, "jitter": 0} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    writes()
    latency_analysis()

    # HEAL NETWORK CONNECTION
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_5")
    #requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency")

def ten_percent_latency():
    print("==============================10% LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_10",
        "type": "latency",
        "attributes": {"latency": 10000, "jitter": 0} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    writes()
    latency_analysis()

    # HEAL NETWORK CONNECTION
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_10")

def twenty_five_percent_latency():
    print("==============================25% LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_25",
        "type": "latency",
        "attributes": {"latency": 25000, "jitter": 0} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    writes()
    latency_analysis()

    # HEAL NETWORK CONNECTION
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_25")

def latency_analysis():
    global latency_arr
    arr = np.array(latency_arr)
    results = np.percentile(arr, [50,99])
    print(f"Latency Percentile Results (p50 & p99): {results}")
    latency_arr.clear()

def main():
    #baseline()
    five_percent_latency()
    ten_percent_latency()
    twenty_five_percent_latency()

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