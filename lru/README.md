Course: Digital Fundamentals and Computer Architecture & Advanced Software Engineering 
Assignment: Simulating Cache Memory Mapping and Replacement Algorithms using Git Collaboration 
Branch Name: lru_module All LRU-related source code, documentation, flow diagrams, and simulation files are maintained in this branch.

PROJECT TITLE:LRU Cache REPLACEMENT ALGORITHM SIMULATIOM

RINTA THOMAS
Team 11 – LRU Module

ROLE: LRU  Algorith Documentation And Implementation


## Description
This module implements the Least Recently Used (LRU) cache replacement policy.
The Least Recently Used (LRU) cache replacement algorithm is a memory management technique used to decide which items to remove from a cache when it reaches its capacity. LRU operates on the principle that the data that has not been used for the longest time is least likely to be used in the near future, so it is the first candidate for removal.
This algorithm maintains the order of usage of cached items, updating their “recently used” status on each access. When the cache is full and a new item needs to be inserted, the least recently accessed item is evicted to make space.

## Capacity
Cache capacity is fixed and removes the least recently accessed item when full.
he capacity of an LRU cache refers to the maximum number of items it can hold at any given time. 
Once the cache reaches this limit, adding a new item requires evicting the least recently used item to make space.

## Operations.
get(key) – Retrieve a value from the cache:
If the key exists in the cache, return the value.
Mark the key as most recently used.
If the key does not exist, return -1 or null (cache miss)

put(key, value) – Insert or update a value in the cache:
If the key already exists, update its value and mark it as most recently used.
If the key does not exist:
If the cache has not reached capacity, simply add it.
If the cache is full, evict the least recently used (LRU) item before adding the new item

## ExampleIf the cache is full, evict the least recently used (LRU) item before adding the new item.

Cache Capacity = 3
put(1, A)
put(2, B)
put(3, C)
get(2) → moves 2:B to MRU
put(4, D) → removes 1:A





Advantages of LRU (Least Recently Used) Replacement Algorithm

.Good Performance
LRU removes the page that has not been used for the longest time.
This matches real program behavior, where recently used pages are likely to be used again.

.Low Page Fault Rate
Compared to FIFO, LRU generally produces fewer page faults.

.No Belady’s Anomaly
Increasing the number of frames never increases page faults in LRU.

.Widely Used Concept
Used in operating systems, CPU caches, and database caching systems.

.Predictable Behavior
Replacement decision is logical and consistent based on usage history.


Disadvantages 

.High Implementation Cost
Requires tracking every page access.

Needs extra hardware or complex data structures (stack, linked list, counters).
.More Memory Overhead

Additional space is required to store usage order or timestamps.
.Slower Than FIFO

Updating access information on every memory reference increases overhead.
'Not Always Optimal

Past behavior may not always predict future usage accurately.
.Complex for Large Systems

Difficult to implement efficiently when the cache size is very large.

## 🎞️ LRU Cache Simulation Demo

![LRU Cache Simulation](lru.gif)
