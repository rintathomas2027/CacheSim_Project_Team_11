FIFO Cache Replacement Simulation

Module Name
FIFO Cache Replacement Module (`fifo_module`)

Subject
24MCAT103 – Digital Fundamentals and Computer Architecture**
24MCAT107 – Advanced Software Engineering**

Project Overview
This module simulates the FIFO (First-In-First-Out) cache replacement algorithm using an array-based implementation.  
The simulation demonstrates how memory blocks are inserted and removed from the cache based on their arrival order.

The FIFO policy removes the oldest block in the cache when the cache becomes full and a new block needs to be loaded.

Algorithm (FIFO)
1. Initialize an empty cache array.
2. For each memory reference:
   - If the block is already in cache → Count as **Hit**
   - Else → **Miss**
     - If cache is full → Remove the oldest block
     - Insert the new block at the end
3. Display cache content after each access.
4. Calculate hits, misses, and hit ratio.
