

def lru_cache_simulation(reference_string, cache_size):
    cache = []
    hits = 0
    misses = 0

    print("Reference\tCache State\t\tHit/Miss")
    print("-" * 45)

    for block in reference_string:
        if block in cache:
            hits += 1
           
            cache.remove(block)
            cache.append(block)
            result = "HIT"
        else:
            misses += 1
          
            if len(cache) == cache_size:
                cache.pop(0)
            cache.append(block)
            result = "MISS"

        print(f"{block}\t\t{cache}\t\t{result}")

    hit_ratio = hits / len(reference_string)

    print("\nTotal Hits   :", hits)
    print("Total Misses:", misses)
    print("Hit Ratio   :", hit_ratio)



reference_string = [1, 2, 3, 4, 1, 2, 5]
cache_size = 3

lru_cache_simulation(reference_string, cache_size)
