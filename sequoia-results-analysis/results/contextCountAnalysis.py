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
# Get time taken for each test from 'v0-ExecutorNoAkka-MultiQueueExecutor-32core-results.txt'
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

noZeroes = {k: v for k, v in contextCount.items() if v != 0} # Filter out tests that timed out during the context count test (context count = 0)

# -------------------
# Get the time taken for each test from 'MultiQueueExecutor-core-results.txt'
# -------------------
multiQueue1coreResults = {}
multiQueue32coreResults = {}
with open('MultiQueueExecutor-core-results.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[0][85:89]
        if 'FAIL' in line: continue
        elif 'TIMEOUT' in line: time = 600_000
        else: time = int(parts[4])

        if "1core" in parts[1]:
            multiQueue1coreResults[problem_number] = time
        elif "Unbounded" in parts[1]:
            multiQueue32coreResults[problem_number] = time

# -------------------
# Plot scatter graph of speedup (v0 time / ExecutorNoAkka time) (y-axis) vs number of contexts created (x-axis)
# On same axis, plot speedup (v0 time / MultiQueueExecutor time) (y-axis) vs number of contexts created (x-axis)
# -------------------
executorNoAkkaSpeedup = np.array([[int(noZeroes[k]), v0results[k] / executorNoAkkaResults[k]] for k in noZeroes])
multiQueueExecutorSpeedup = np.array([[int(noZeroes[k]), v0results[k] / multiQueueExecutorResults[k]] for k in noZeroes])

plt.scatter(executorNoAkkaSpeedup[:,0], executorNoAkkaSpeedup[:,1], label="ExecutorNoAkka", color='b')
plt.scatter(multiQueueExecutorSpeedup[:,0], multiQueueExecutorSpeedup[:,1], label="MultiQueueExecutor", color='r')

# Lines of best fit
xnew = np.linspace(min(executorNoAkkaSpeedup[:,0]), max(executorNoAkkaSpeedup[:,0]), 50)
# - ExecutorNoAkka
z = np.polyfit(np.log(executorNoAkkaSpeedup[:,0]), np.log(executorNoAkkaSpeedup[:,1]), 1)
f = np.poly1d(z)
plt.plot(xnew, np.exp(f(np.log(xnew))), 'b--')
# - MultiQueueExecutor
z = np.polyfit(np.log(multiQueueExecutorSpeedup[:,0]), np.log(multiQueueExecutorSpeedup[:,1]), 1)
f = np.poly1d(z)
plt.plot(xnew, np.exp(f(np.log(xnew))), 'r--')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of contexts created')
plt.ylabel('Speedup (v0 time / new implementation time)')
plt.legend()
plt.title('Speedup vs Number of contexts created (32 cores)')
plt.show()
 
# -------------------
# Plot scatter graph of speedup (ExecutorNoAkka-1core time / ExecutorNoAkka time) (y-axis) vs number of contexts created (x-axis)
# On same axis, plot speedup (MultiQueueExecutor-1core time / MultiQueueExecutor time) (y-axis) vs number of contexts created (x-axis)
# -------------------
multiQueue1coreSpeedup = np.array([[int(noZeroes[k]), v0results[k] / multiQueue32coreResults[k]] for k in noZeroes])

plt.scatter(multiQueue1coreSpeedup[:,0], multiQueue1coreSpeedup[:,1], label="MultiQueueExecutor", color='r')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of contexts created')
plt.ylabel('Speedup (CSO time / MultiQueueExecutor time)')
# plt.legend()
plt.title('Scatter graph of speedup vs context-count (32 cores)')
plt.show()


# -------------------
# As a different graph, plot context count vs time taken for ExecutorNoAkka, MultiQueueExecutor, and v0
# -------------------
executorNoAkkaTimeTaken = np.array([[int(noZeroes[k]), executorNoAkkaResults[k]] for k in noZeroes])
multiQueueExecutorTimeTaken = np.array([[int(noZeroes[k]), multiQueueExecutorResults[k]] for k in noZeroes])
v0TimeTaken = np.array([[int(noZeroes[k]), v0results[k]] for k in noZeroes])

plt.scatter(v0TimeTaken[:,0], v0TimeTaken[:,1], label="CSO", color='g')
plt.scatter(executorNoAkkaTimeTaken[:,0], executorNoAkkaTimeTaken[:,1], label="SingleQueueExecutor", color='b')
plt.scatter(multiQueueExecutorTimeTaken[:,0], multiQueueExecutorTimeTaken[:,1], label="MultiQueueExecutor", color='r')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of contexts created')
plt.ylabel('Time taken (ms)')
plt.legend()
plt.title('Scatter graph of time taken vs context-count (32 cores)')
plt.show()