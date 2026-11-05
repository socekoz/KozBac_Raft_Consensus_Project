**Environment Lifecycle Commands**
1. Before you begin make sure the docker containers are up and running:
   1. Start Cluster: ``sudo docker compose up -d`` (first time running this command may take some time)
   2. View Container Status: ``sudo docker ocmpose ps``
2. When you want to reset the state of the docker containers do the following:
   1. Tear Down & Reset State: ``sudo docker compose down -v``

**Fault Injection**
1. Go to ``src`` directory with ``cd src``
2. In the ``src`` directory, run ``python3 inject.py`` in the terminal

**Toxyproxy**
1. Information about Shopify/toxyproxy [here](https://github.com/shopify/toxiproxy)