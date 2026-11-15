Deliverable: Plot p50 and p99 client-observed write latencies as a function of packet loss rate. Explain why p99 degrades faster than p50. 

**Plots for p50 and p99**
1. Go to ``src`` directory: ``cd src``
2. Run file: ``python3 exercise-3.py``
2. See ``.png`` files under ``exercise3-files`` directory for percentiles corresponding to each percentage of packet loss rates
- ``exercise3-5.png`` - 5% latency test
- ``exercise3-10.png`` -  10% latency test
- ``exercise3-25.png`` - 25% latency test
- ``exercise3-all.png`` - 5%, 10%, 25% latency toxics injected together

**Explain why p99 degrades faster than p50**
Before we can understand why p99 degrades faster than p50, we must first understand what those percentiles represent.
In words, p50 shows that 50% of all key-value write requests have latencies at or under a value n (in milliseconds), while p90 
shows that 90% of all key-value write requests have latencies at or under another value m (in milliseconds). 

With that being said, assuming "degradation" in this case refers to the increase in latency associated with p99 
when compared to p50, p99 degrades faster than p50 because it encompasses more key-value write requests, allowing more
key-value write requests with greater latencies to be captured and, thus, included in p90, plotting it high in a percentile graph. 
On the other hand, p50 captures a smaller number of key-value write requests and, thus, would represent key-value write requests 
with smaller latencies, plotting it lower in a percentile graph.