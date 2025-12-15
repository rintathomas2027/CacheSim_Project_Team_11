def lfu_cache(reference_string, cache_size):
    cache = []                 # Stores cache blocks
    frequency = {}              # Stores frequency of each block
    order = {}                  # Stores arrival order for tie-breaking
    time = 0

    hits = 0
    misses = 0

    print("Ref\tCache\t\tStatus")

    for ref in reference_string:
        time += 1

        # Cache HIT
        if ref in cache:
            hits += 1
            frequency[ref] += 1
            print(f"{ref}\t{cache}\tHIT")

        # Cache MISS
        else:
            misses += 1

            # If cache has space
            if len(cache) < cache_size:
                cache.append(ref)
                frequency[ref] = 1
                order[ref] = time

            # Cache full → apply LFU replacement
            else:
                # Find least frequently used item
                min_freq = min(frequency[x] for x in cache)

                # Items with minimum frequency
                lfu_items = [x for x in cache if frequency[x] == min_freq]

                # Tie-breaking using FIFO (oldest entry)
                victim = min(lfu_items, key=lambda x: order[x])

                cache.remove(victim)
                del frequency[victim]
                del order[victim]

                cache.append(ref)
                frequency[ref] = 1
                order[ref] = time

            print(f"{ref}\t{cache}\tMISS")

    hit_ratio = hits / (hits + misses)

    print("\nTotal Hits:", hits)
    print("Total Misses:", misses)
    print("Hit Ratio:", round(hit_ratio, 2))


# Example usage
reference_string = [1, 2, 3, 2, 4, 1, 5, 2, 1, 2]
cache_size = 3

lfu_cache(reference_string, cache_size)
