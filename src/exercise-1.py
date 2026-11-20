import requests
import time
import json
import pprint
import numpy as np
from matplotlib import mlab
import matplotlib.pyplot as plt

latency_arr = []
latency_arr_overall = []

def all_latency():
    global latency_arr
    global latency_arr_overall
    print("==============================50 ms, 100 ms, 300 ms LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_50",
        "type": "latency",
        "attributes": {"latency": 50, "jitter": 0} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul2/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul3/toxics", json=payload)

    payload = {
            "name": "latency_100",
            "type": "latency",
            "attributes": {"latency": 100, "jitter": 0} # 10% latency
        }

    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul2/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul3/toxics", json=payload)

    payload = {
            "name": "latency_300",
            "type": "latency",
            "attributes": {"latency": 300, "jitter": 0} # 25% latency
        }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul2/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul3/toxics", json=payload)

    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    #writes()
    #latency_analysis(latency_arr)
    #plot_percentiles(1, "exercise1-files/exercise1-all")
    #latency_arr.clear()
    #latency_arr_overall.clear()

    # HEAL NETWORK CONNECTION
    i = 1
    while i < 4:
        requests.delete(f"{TOXIPROXY_API}/proxies/consul{i}/toxics/latency_50")
        requests.delete(f"{TOXIPROXY_API}/proxies/consul{i}/toxics/latency_100")
        requests.delete(f"{TOXIPROXY_API}/proxies/consul{i}/toxics/latency_300")
        i += 1
    #requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency")
    get_metrics()

def fifty_latency():
    global latency_arr
    print("==============================50 ms LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_50",
        "type": "latency",
        "stream": "upstream",
        "attributes": {"latency": 50, "jitter": 0} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul2/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul3/toxics", json=payload)

    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    #writes()
    #latency_analysis(latency_arr)
    #plot_percentiles(2, "exercise1-files/exercise1-50")
    #latency_arr.clear()

    #time.sleep(120)

    # HEAL NETWORK CONNECTION
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_50")
    requests.delete(f"{TOXIPROXY_API}/proxies/consul2/toxics/latency_50")
    requests.delete(f"{TOXIPROXY_API}/proxies/consul3/toxics/latency_50")
    get_metrics()

def one_hundred_latency():
    global latency_arr
    print("==============================100 ms LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_100",
        "type": "latency",
        "stream": "upstream",
        "attributes": {"latency": 100, "jitter": 0} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul2/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul3/toxics", json=payload)

    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    #writes()
    #latency_analysis(latency_arr)
    #plot_percentiles(3, "exercise1-files/exercise1-100")
    #latency_arr.clear()

    #time.sleep(120)

    # HEAL NETWORK CONNECTION
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_100")
    requests.delete(f"{TOXIPROXY_API}/proxies/consul2/toxics/latency_100")
    requests.delete(f"{TOXIPROXY_API}/proxies/consul3/toxics/latency_100")
    get_metrics()

def three_hundred_latency():
    global latency_arr
    print("==============================300 ms LATENCY============================")
    TOXIPROXY_API = "http://localhost:8474" # injection
    payload = {
        "name": "latency_300",
        "type": "latency",
        "stream": "upstream",
        "attributes": {"latency": 300, "jitter": 0} # 5% latency
    }
    # INJECT TOXIC
    requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul2/toxics", json=payload)
    requests.post(f"{TOXIPROXY_API}/proxies/consul3/toxics", json=payload)

    json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
    print(json_data.json())

    #writes()
    #latency_analysis(latency_arr)
    #plot_percentiles(4, "exercise1-files/exercise1-300")
    #latency_arr.clear()

    #time.sleep(120)

    # HEAL NETWORK CONNECTION
    requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_300")
    requests.delete(f"{TOXIPROXY_API}/proxies/consul2/toxics/latency_300")
    requests.delete(f"{TOXIPROXY_API}/proxies/consul3/toxics/latency_300")
    get_metrics()

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

def get_metrics():
    TOXIPROXY_API = "http://localhost:8500" # metrics
    # pretty print dictionary
    pp = pprint.PrettyPrinter(indent=1, width=20)
    json_data = requests.get(f"{TOXIPROXY_API}/v1/agent/metrics")

    pp.pprint(json_data.json())
    #print(json_data.json())

def main():
    #baseline()
    global latency_arr
    #all_latency()
    fifty_latency()
    one_hundred_latency()
    three_hundred_latency()
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