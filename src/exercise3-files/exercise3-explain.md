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
Before we can understand why p99 degrades faster than p50, we must first understand what those percentiles represent.
In words, p50 shows that 50% of all key-value write requests have latencies at or under a value n (in milliseconds), while p99
shows that 99% of all key-value write requests have latencies at or under another value m (in milliseconds). 

With that being said, assuming "degradation" in this case refers to the decrease in latency associated with p99 
when compared to p50 across all packet loss rates, p99 degrades faster than p50 because p99 effectively represents 
the maximum value that a latency can be for a given packet loss rate. So, for a packet loss rate of 5% the maximum value in 
milliseconds (ms) that 99% of latencies could be is 0.7 ms, while for a packet loss rate of 10% the maximum value in 
milliseconds (ms) that 99% of latencies could be is 0.2 ms, and for a packet loss rate of 25% the maximum value in 
milliseconds (ms) that 99% of latencies could be is 0.15 ms. Now, considering latencies for p99 for packet loss rates of 
5%, 10%, and 25%, respectively, it demonstrates that, overall, the highest latency that a given packet loss rate can get 
decreases/degrades as packet loss rates get higher, possibly due to (1) most packets responding quickly despite the latency 
toxics injected, causing the low latency recordings for both 10% and 25% packet loss compared to the higher latency 
recordings for 5% packet loss, or (2) there is less variability in latency for both 10% and 25% packet loss rates, as 
a larger margin exists between their respective p50 and p99 recordings, compared to the variability in latency for 
5% packet loss rate, where a smaller margin exists between its p50 and p99 recordings.
