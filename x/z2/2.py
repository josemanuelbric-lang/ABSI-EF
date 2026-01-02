import time
import random
from core import resolver_mochila

random.seed(42)
item_count = 4096
max_capacity = 12 

values_list = [random.randint(1, 1000) for _ in range(item_count)]
weights_list = [random.randint(1, 1000) for _ in range(item_count)]

start = time.perf_counter()
result = resolver_mochila(weights_list, values_list, max_capacity)
end = time.perf_counter()

print(f"Max Value Found: {result}")
print(f"Execution Time: {end - start:.6f} seconds")