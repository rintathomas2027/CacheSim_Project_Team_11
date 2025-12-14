
Team 11 – LRU Module

LRU Cache Replacement Simulation

Module Name: LRU Cache Replacement Module (lru_module)

 Objective: To simulate the Least Recently Used (LRU) Cache Replacement Algorithm and analyze cache performance by calculating hits, misses, and hit ratio.

 Concept :LRU replaces the memory block that has not been used for the longest time.

Frequently accessed blocks are kept in cache.

More efficient than FIFO because it considers recent usage.

 LRU Algorithm 

Initialize an empty cache of fixed size.

For each memory reference:

If the block is already in cache → Hit

Move the block to the most recently used position.

Else → Miss

If cache is full:

Remove the least recently used block.

Insert the new block as the most recently used.

Display cache contents after each access.

Calculate:

Total Hits

Total Misses

Hit Ratio = Hits / Total References

 LRU Example
Cache Size = 3
Memory Reference String:1 2 3 4 1 2 5

Step	Block	Cache State (LRU → MRU)	Hit/Miss
1	1	1	Miss
2	2	1 2	Miss
3	3	1 2 3	Miss
4	4	2 3 4	Miss
5	1	3 4 1	Miss
6	2	4 1 2	Miss
7	5	1 2 5	Miss


 Performance Calculation

Total References: 7

Hits: 0

Misses: 7

Hit Ratio: 0 / 7 = 0

 Advantages of LRU:

Better cache utilization

Reduces cache misses

Reflects real program behavior

Widely used in operating systems and processors

 Disadvantages:

Requires tracking usage history

Slightly complex implementation

Higher overhead than FIFO

 Applications:

CPU cache management

Operating systems (page replacement)

Database buffer management

Web caching systems


The LRU cache replacement algorithm improves cache performance by retaining recently used memory blocks, making it more efficient and practical than FIFO.

