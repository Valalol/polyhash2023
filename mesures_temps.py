from time import *
from mathematiks import *

# Start timer
start_time = time()

for _ in range(10000000):
    taille = 1000

# End timer
end_time = time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)