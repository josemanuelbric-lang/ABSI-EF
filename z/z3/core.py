# core.py
import time

class _InternalItem:
    def __init__(self, w, v):
        self.w = w
        self.v = v
        self.d = v / w 

def solve_fast(weights, values, capacity):
    # Optimized structural approach
    items = [_InternalItem(weights[i], values[i]) for i in range(len(weights))]
    items.sort(key=lambda x: x.d, reverse=True)
    
    max_val = 0
    active_nodes = [(0, 0)] 
    
    for item in items:
        next_nodes = []
        for current_w, current_v in active_nodes:
            if current_w + item.w <= capacity:
                new_v = current_v + item.v
                next_nodes.append((current_w + item.w, new_v))
                if new_v > max_val: 
                    max_val = new_v
            next_nodes.append((current_w, current_v))
        
        active_nodes = next_nodes
        if len(active_nodes) > 1000:
            active_nodes.sort(key=lambda x: x[1], reverse=True)
            active_nodes = active_nodes[:500]
    return max_val

def solve_standard(weights, values, capacity, n):
    # Classic brute force (recursive)
    if n == 0 or capacity == 0:
        return 0
    if weights[n-1] > capacity:
        return solve_standard(weights, values, capacity, n-1)
    else:
        return max(
            values[n-1] + solve_standard(weights, values, capacity - weights[n-1], n-1),
            solve_standard(weights, values, capacity, n-1)
        )