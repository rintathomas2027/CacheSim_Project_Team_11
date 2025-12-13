# LRU Cache Module

## Description
This module implements the Least Recently Used (LRU) cache replacement policy.

## Capacity
Cache capacity is fixed and removes the least recently accessed item when full.

## Operations
- put(key, value)
- get(key)

## Example
Cache Capacity = 3
put(1, A)
put(2, B)
put(3, C)
get(2) → moves 2:B to MRU
put(4, D) → removes 1:A

## Author
Team 11 – LRU Module
