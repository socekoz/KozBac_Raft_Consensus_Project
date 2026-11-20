import requests
import time
import json
import pprint
import numpy as np
from matplotlib import mlab
import matplotlib.pyplot as plt

latency_arr = []
latency_arr_overall = []

def writes():
    global latency_arr
    global latency_arr_overall
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
        latency_arr_overall.append(latency)
        i += 1

def all_latency():
    global latency_arr
    global latency_arr_overall
    print("==============================5% LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_5",
        "type": "latency",
        "attributes": {"latency": 0, "jitter": 50} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)

    payload = {
            "name": "latency_10",
            "type": "latency",
            "attributes": {"latency": 0, "jitter": 100} # 10% latency
        }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)

    payload = {
            "name": "latency_25",
            "type": "latency",
            "attributes": {"latency": 0, "jitter": 250} # 25% latency
        }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)

    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    writes()
    latency_analysis(latency_arr)
    plot_percentiles(1, "exercise3-files/exercise3-all")
    latency_arr.clear()
    latency_arr_overall.clear()

    # HEAL NETWORK CONNECTION
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_5")
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_10")
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_25")
    #requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency")

def five_percent_latency():
    global latency_arr
    print("==============================10% LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_5",
        "type": "latency",
        "attributes": {"latency": 0, "jitter": 50} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    writes()
    latency_analysis(latency_arr)
    plot_percentiles(2, "exercise3-files/exercise3-5")
    latency_arr.clear()

    # HEAL NETWORK CONNECTION
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_5")

def ten_percent_latency():
    global latency_arr
    print("==============================10% LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_10",
        "type": "latency",
        "attributes": {"latency": 0, "jitter": 100} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    writes()
    latency_analysis(latency_arr)
    plot_percentiles(3, "exercise3-files/exercise3-10")
    latency_arr.clear()

    # HEAL NETWORK CONNECTION
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_10")

def twenty_five_percent_latency():
    global latency_arr
    print("==============================25% LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_25",
        "type": "latency",
        "attributes": {"latency": 0, "jitter": 250} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    writes()
    latency_analysis(latency_arr)
    plot_percentiles(4, "exercise3-files/exercise3-25")
    latency_arr.clear()

    # HEAL NETWORK CONNECTION
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_25")

def latency_analysis(array_input):
    #global latency_arr
    arr = np.array(array_input)
    results = np.percentile(arr, [50,99])
    print(f"Latency Percentile Results (p50 & p99): {results}")
    #.clear()

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

def main():
    #baseline()
    global latency_arr
    all_latency()
    five_percent_latency()
    ten_percent_latency()
    twenty_five_percent_latency()
    #latency_analysis(latency_arr_overall)
    #plot_percentiles()
    #latency_arr.clear()

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