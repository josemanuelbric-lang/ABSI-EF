import time
import random

# --- ABSI-EF LOGIC ---
class EFObject:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.density = value / weight

def solve_knapsack_absi_pro(objects, capacity):
    # Sort objects by density (value/weight ratio)
    objects.sort(key=lambda x: x.density, reverse=True)
    best_value = 0
    active_nodes = [(0, 0, "N")]  # (current_weight, current_value, path)
    
    for obj in objects:
        next_nodes = []
        for current_weight, current_value, path in active_nodes:
            # Right branch: Take the object
            if current_weight + obj.weight <= capacity:
                new_value = current_value + obj.value
                next_nodes.append((current_weight + obj.weight, new_value, path + "R"))
                if new_value > best_value:
                    best_value = new_value
            # Left branch: Skip the object
            next_nodes.append((current_weight, current_value, path + "L"))
        
        active_nodes = next_nodes
        
        # Prune if too many nodes (maintain efficiency)
        if len(active_nodes) > 1000:
            active_nodes.sort(key=lambda x: x[1], reverse=True)
            active_nodes = active_nodes[:500]
    
    return best_value

# --- BRUTE FORCE LOGIC (Exponential) ---
def brute_force_recursive(objects, capacity, n):
    # Base case: no objects left or no capacity
    if n == 0 or capacity == 0:
        return 0
    
    # If object weighs more than capacity, skip it (forced Left branch)
    if objects[n-1].weight > capacity:
        return brute_force_recursive(objects, capacity, n-1)
    else:
        # Try both possibilities: Take (R) and Skip (L)
        return max(
            objects[n-1].value + brute_force_recursive(objects, capacity - objects[n-1].weight, n-1),
            brute_force_recursive(objects, capacity, n-1)
        )

# --- COMPARISON TEST ---
random.seed(42)
n_objects = 22  # Reduced to 22 so brute force doesn't freeze
test_objects = [EFObject(random.randint(1, 20), random.randint(10, 100)) for _ in range(n_objects)]
test_capacity = 100

print(f"Comparing {n_objects} objects...\n")

# Execute ABSI-EF
start = time.perf_counter()
absi_result = solve_knapsack_absi_pro(test_objects, test_capacity)
absi_time = time.perf_counter() - start

# Execute Brute Force
start = time.perf_counter()
brute_result = brute_force_recursive(test_objects, test_capacity, n_objects)
brute_time = time.perf_counter() - start

print(f"--- RESULTS ---")
print(f"ABSI-EF:      Value {absi_result} | Time: {absi_time:.6f} sec")
print(f"Brute Force:  Value {brute_result} | Time: {brute_time:.6f} sec")
print(f"Speed difference: {brute_time / absi_time:.2f}x faster for ABSI-EF")
