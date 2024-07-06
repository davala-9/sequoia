import matplotlib.pyplot as plt
import numpy as np

# -------------------
# Get number of contexts created for each test from 'ContextCountResults.txt'
# -------------------
contextCount = {str(i).zfill(5): 0 for i in range(1, 800)}
with open('ContextCountResults.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[0][65:69]
        contextCount[problem_number] = int(parts[6]) # Note: if the test timed out, the context count is 0. We will ignore these results in charts

# -------------------
# Plot scatter graph of speedup (v0 time / ExecutorNoAkka time) (y-axis) vs number of contexts created (x-axis)
# On same axis, plot speedup (v0 time / MultiQueueExecutor time) (y-axis) vs number of contexts created (x-axis)
# -------------------
v0results = {}
executorNoAkkaResults = {}
multiQueueExecutorResults = {}
with open('v0-ExecutorNoAkka-MultiQueueExecutor-32core-results.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[0][85:89]
        if 'TIMEOUT' in line: time = 600_000
        else: time = int(parts[4])

        if "OLD" in parts[1]:
            v0results[problem_number] = time
        elif "EXECUTORnoakkasequoia" in parts[1]:
            executorNoAkkaResults[problem_number] = time
        elif "FUNKY" in parts[1]:
            multiQueueExecutorResults[problem_number] = time
        else:
            print("Error: unknown result")
            quit()

print(v0results)
print()
print(executorNoAkkaResults)
print()
print(multiQueueExecutorResults)



# -------------------
# As a different graph, plot context count vs time taken for ExecutorNoAkka, MultiQueueExecutor, and v0
# -------------------