def fifo_cache_simulation(cache_size, reference_string):
    cache = [] 
    hits = 0
    misses = 0

    print("\nFIFO Cache Simulation")
    print("-----------------------")

    for item in reference_string:
        print(f"\nAccessing: {item}")

        if item in cache:
            hits += 1
            print("Status: HIT")
        else:
            misses += 1
            print("Status: MISS")

            if len(cache) == cache_size:
                removed = cache.pop(0)
                print(f"Removed (Oldest): {removed}")

            cache.append(item)

        print(f"Cache State: {cache}")

    total = hits + misses
    hit_ratio = hits / total if total > 0 else 0

    print("\n--- Simulation Summary ---")
    print(f"Reference String: {reference_string}")
    print(f"Cache Size: {cache_size}")
    print(f"Total Hits : {hits}")
    print(f"Total Misses : {misses}")
    print(f"Hit Ratio : {hit_ratio:.2f}")
    print(f"Final Cache : {cache}")


cache_size = 3

reference_string = ['A', 'B', 'C', 'A', 'B', 'C', 'D', 'A', 'B']

fifo_cache_simulation(cache_size, reference_string)
