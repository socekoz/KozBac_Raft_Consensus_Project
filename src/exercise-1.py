import requests
import time
import json
import pprint
import threading
import numpy as np
from matplotlib import mlab
import matplotlib.pyplot as plt

election_frequency_arr = []
latency_arr = []

def latency_test(latency):
    global latency_arr
    global election_frequency_arr
    print("==============================LATENCY TEST START============================")

    # INJECT TOXIC
    i = 1
    while (i < 100):
        TOXIPROXY_API = "http://localhost:8474" # injection
        payload = {
            "name": f"latency_{i}",
            "type": "latency",
            "stream": "upstream",
            "attributes": {"latency": i*latency, "jitter": 0} # i.e. increasing latency by 50 ms after each loop
        }
        latency_arr.append(i*latency)

        # inject toxics
        requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload)
        requests.post(f"http://localhost:8475/proxies/consul2/toxics", json=payload)
        requests.post(f"http://localhost:8476/proxies/consul3/toxics", json=payload)


        # verify toxics were created
        json_data = requests.get(f"{TOXIPROXY_API}/proxies/consul1/toxics")
        print(json_data.json())
        time.sleep(5)
        json_data = requests.get(f"http://localhost:8475/proxies/consul2/toxics")
        print(json_data.json())
        time.sleep(5)
        json_data = requests.get(f"http://localhost:8476/proxies/consul3/toxics")
        print(json_data.json())

        pp = pprint.PrettyPrinter(indent=1, width=20)
        j = 0
        election_count = 0
        current_leader_data = requests.get(f"http://localhost:8500/v1/status/leader")
        current_leader = current_leader_data.json()
        print(current_leader)
        while (j < 10):
            new_leader_data = requests.get(f"http://localhost:8500/v1/status/leader")
            print(new_leader_data.json())
            if(current_leader != new_leader_data.json()):
                election_count += 1
                current_leader = new_leader_data.json()
            time.sleep(10)
            j += 1
        election_frequency_arr.append(election_count)
        print(election_frequency_arr)
        print(latency_arr)

        # clean up
        requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_{i}")
        requests.delete(f"http://localhost:8475/proxies/consul2/toxics/latency_{i}")
        requests.delete(f"http://localhost:8476/proxies/consul3/toxics/latency_{i}")

        i += 1

def main():
    global latency_arr
    latency_test(50)

main()