Deliverable: Plot p50 and p99 client-observed write latencies as a function of packet loss rate. Explain why p99 degrades faster than p50. 

**Plots for p50 and p99**
1. Go to ``src`` directory: ``cd src``
2. Run file: ``python3 exercise-3.py``
2. See ``.png`` files under ``exercise3-files`` directory for percentiles corresponding to each percentage of packet loss rates
- ``exercise3-5.png`` - 5% latency test
- ``exercise3-10.png`` -  10% latency test
- ``exercise3-25.png`` - 25% latency test
- ``exercise3-all.png`` - 5%, 10%, 25% latency toxics injected together

![percentile plots](exercise3-plot.pdf)

**Explain why p99 degrades faster than p50**
Before we can understand why p99 degrades faster than p50, we must first understand what those percentiles 
represent with respect to the packet loss rates that they are associated with. In words, p50 shows that 50% 
of all key-value write requests for 5%, 10%, and 25% packet loss rates have latencies at or under a value 
n (in milliseconds), while p99 shows that 99% of all key-value write requests for 5%, 10%, and 25% packet 
loss rates have latencies at or under another value m (in milliseconds). 

Based on the plotted points on the graph provided, there is a trend, from 5% packet loss to 10% packet loss, 
showing how p99 appears to degrade, or decrease, in latency when higher rates of packet loss are injected 
into the network. The reason for this increased degradation could be due to the packet loss rates injected.
As packet loss rates go up, it is expected to see a positively correlated change in the latency of key-value write 
requests as a result. With that, more and more requests are experiencing greater latencies, meaning that p99 would
have to become smaller in order to accommodate for this change, as a higher percentile (i.e. p100) would capture
higher latencies (capturing the smaller portion of requests that have very high latencies). 
