import time
import random
from core import solve_fast, solve_standard

random.seed(42)
n = 32
capacity = 50

values = [random.randint(10, 100) for _ in range(n)]
weights = [random.randint(1, 20) for _ in range(n)]


start = time.perf_counter()
res_fast = solve_fast(weights, values, capacity)
time_fast = time.perf_counter() - start
print(f"Fast Solver:     Value {res_fast} | Time: {time_fast:.6f}s")

start = time.perf_counter()
res_std = solve_standard(weights, values, capacity, n)
time_std = time.perf_counter() - start
print(f"Standard Solver: Value {res_std} | Time: {time_std:.6f}s")

print("-" * 45)
if time_fast > 0:
    print(f"Speed Factor: {time_std / time_fast:.2f}x faster")