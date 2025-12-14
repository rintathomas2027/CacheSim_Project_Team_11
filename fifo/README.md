Course: Digital Fundamentals and Computer Architecture & Advanced Software Engineering

Assignment: Simulating Cache Memory Mapping and Replacement Algorithms using Git Collaboration

Branch Name: fifo_module

All FIFO-related source code, documentation, flow diagrams, and simulation files are maintained in this branch.

1. Project Title

  FIFO Cache Replacement Algorithm Simulation

2. Objective

  The objective of this module is to simulate the FIFO (First-In First-Out) cache replacement algorithm and demonstrate its working using a reference string and     fixed cache size.
  This module also supports the practical application of Git version control for collaborative software development as required by the assignment guidelines.

3. Description of FIFO Module

  The FIFO module simulates how cache memory handles page replacement using the First-In First-Out policy.
  When the cache is full and a new memory block needs to be inserted, the oldest block present in the cache is removed, regardless of how frequently it has been     accessed.

  This simulation:

  Tracks hits and misses

  Displays cache state after each memory access

  Calculates hit ratio

  Visually represents FIFO behavior using diagrams and animation

4. Brief Explanation of FIFO Algorithm

  FIFO (First-In First-Out) is one of the simplest cache replacement algorithms.

  Working Principle:

  Pages are loaded into the cache in the order they arrive.

  When the cache becomes full:

  The page that entered the cache earliest is removed.

  FIFO does not consider usage frequency, only arrival order.

  Advantages:

  Simple to implement

  Low overhead

  Disadvantages:

  May remove frequently used pages

  Can lead to poor performance in some cases

5. Team Member Name and Role
   
  Name	 Sainu Anna Sajan
  
  Role   FIFO Algorithm Implementation & Documentation

