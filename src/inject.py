import requests
import time
import json
import pprint

TOXIPROXY_API = "http://localhost:8474" # injection
payload = {
    "name": "latency_toxic",
    "type": "latency",
    "attributes": {"latency": 300, "jitter": 50}
}
# INJECT TOXIC
print(requests.post(f"{TOXIPROXY_API}/proxies/consul1/toxics", json=payload))

# HEAL NETWORK CONNECTION
print(requests.delete(f"{TOXIPROXY_API}/proxies/consul1/toxics/latency_toxic"))

TOXIPROXY_API = "http://localhost:8500" # metrics
# pretty print dictionary
pp = pprint.PrettyPrinter(indent=1, width=20)

# GET METRICS: Cluster stability
json_data = requests.get(f"{TOXIPROXY_API}/v1/agent/metrics")
pp.pprint(json_data.json())

# GET CONFIGURATION: Track state divergence
json_data = requests.get(f"{TOXIPROXY_API}/v1/operator/raft/configuration")
pp.pprint(json_data.json())
