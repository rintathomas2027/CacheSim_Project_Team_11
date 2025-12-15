# Course

**Digital Fundamentals and Computer Architecture & Advanced Software Engineering**

## Assignment

**Simulating Cache Memory Mapping and Replacement Algorithms using Git Collaboration**

---

## Branch Information

* **Branch Name:** `sidharth`
* **Description:** All Set Associative mapping–related source code, documentation, flow diagrams, and simulation files are maintained in this branch.

---

## 1. Project Title

**Set Associative Cache Mapping Simulation**

---

## 2. Objective

The objective of this module is to simulate **Set Associative Cache Mapping** and demonstrate its working using a reference string, fixed cache size, and defined associativity.

This module also highlights the **practical use of Git version control** for collaborative software development as required by the assignment guidelines.

---

## 3. Description of Set Associative Mapping Module

The Set Associative Mapping module simulates how cache memory organizes and accesses memory blocks using a **set-based structure**.

In set associative mapping, the cache is divided into multiple sets, and each set contains a fixed number of cache lines. A memory block maps to **exactly one set**, but it can be placed in **any line within that set**.

### Key Features of the Simulation

* Maps memory blocks to specific cache sets
* Supports configurable **associativity (n-way set associative cache)**
* Tracks **cache hits** and **cache misses**
* Displays **cache contents of each set after every memory access**
* Calculates and displays the **hit ratio**
* Demonstrates replacement within a set (e.g., FIFO/LRU, if implemented)

---

## 4. Brief Explanation of Set Associative Mapping

Set Associative Mapping is a hybrid approach between **Direct Mapping** and **Fully Associative Mapping**.

### Working Principle

* Cache is divided into multiple sets
* Each set contains a fixed number of cache lines (associativity)
* A memory block maps to one specific set using:

  * `Set Number = Block Number mod Number of Sets`
* If the mapped set has an empty line, the block is placed there
* If the set is full:

  * A **replacement policy** (such as FIFO or LRU) is applied **within that set only**

---

## 5. Advantages and Disadvantages

### Advantages

* Reduces conflict misses compared to direct mapping
* Better performance than direct-mapped cache
* Lower complexity than fully associative mapping

### Disadvantages

* More complex than direct mapping
* Requires replacement policy logic within each set
* Slightly higher hardware and implementation cost

---



|

## Conclusion

This Set Associative Cache Mapping simulation provides a balanced approach to cache design by combining flexibility and efficiency. It helps in understanding how memory blocks are distributed across cache sets and how replacement decisions are made within each set, while also reinforcing collaborative development practices using Git.
