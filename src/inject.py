import requests
import time
import json

TOXIPROXY_API = "http://localhost:8474"

payload = {
    "name": "latency_toxic",
    "type": "latency",
    "attributes": {"latency": 300, "jitter": 50}
}

requests.post(f"{TOXIPROXY_API}/proxies/consul_node1/toxics", json=payload)

requests.delete(f"{TOXIPROXY_API}/proxies/consul_node1/toxics/latency_toxic")