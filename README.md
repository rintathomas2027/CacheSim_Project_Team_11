FIFO Cache Replacement Module

Project Title
Simulating Cache Memory Mapping and Replacement Algorithms using Git Collaboration

Description of FIFO Module
This module implements and demonstrates the FIFO (First-In First-Out) Cache Replacement Algorithm as part of a cache memory simulation project.
The FIFO module simulates how memory blocks are loaded into a fixed-size cache and how the oldest block is removed when the cache becomes full.

The implementation provides:
Step-by-step cache simulation
Identification of cache hits and misses
Final cache state and hit ratio calculation
Visual support using flow diagrams and simulation illustrations

Team Member Name & Role
Sainu Anna Sajan – FIFO Module Implementation, Documentation & Visualization
(Team 11 – Cache Simulation Project)

Brief Explanation of FIFO Algorithm
The First-In First-Out (FIFO) cache replacement algorithm replaces the oldest memory block in the cache when a new block needs to be inserted and the cache is already full.

Key Characteristics:
Cache blocks are removed in the order they were added
Simple to implement
Does not consider how frequently or recently a block is used

Working Principle:
If the requested block is already in cache → Hit
If not present → Miss
If cache is full during a miss → Remove the earliest inserted block
Insert the new block at the end of the queue

Branch Name
fifo_module

All FIFO-related source code, documentation, flow diagrams, and simulation files are maintained in this branch.
