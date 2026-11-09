**Environment Lifecycle Commands**
1. Before you begin make sure the docker containers are up and running:
   1. Start Cluster: ``sudo docker compose up -d`` (first time running this command may take some time)
   2. View Container Status: ``sudo docker compose ps``
2. When you want to reset the state of the docker containers do the following:
   1. Tear Down & Reset State: ``sudo docker compose down -v``

**Fault Injection**
1. Go to ``src`` directory with ``cd src``
2. In the ``src`` directory, run ``python3 inject.py`` in the terminal

**Toxyproxy API**
1. Access Consul-UI through ``http://10.99.0.20/8500``, use this for getting Consul metrics
2. Access Consul proxies for injection ``http://localhost:8474``
   1. Example: ``requests.post(f"http://localhost:8474/proxies/consul1/toxics", json=payload)``
   2. General usage: `requests.post(f"http://localhost:8474/proxies/{consul_name}/toxics", json=payload)``
3. Information about Shopify/toxyproxy [here](https://github.com/shopify/toxiproxy)
4. Information about Toxiproxy API [here](https://developer.hashicorp.com/consul/api-docs/agent#view-metrics)