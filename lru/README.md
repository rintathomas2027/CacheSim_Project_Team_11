# LRU Cache Module

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

RINTA THOMAS
Team 11 – LRU Module
## 🎞️ LRU Cache Simulation Demo

![LRU Cache Simulation](lru.gif)
