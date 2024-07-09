import matplotlib.pyplot as plt
import numpy as np

# -------------------
# Get time taken for each test from 'v0-ExecutorNoAkka-MultiQueueExecutor-32core-results.txt'
# -------------------
v0results = {}
with open('v0-ExecutorNoAkka-MultiQueueExecutor-32core-results.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[0][84:89]
        if 'TIMEOUT' in line: time = 600_000
        else: time = int(parts[4])

        if "OLD" in parts[1]:
            v0results[problem_number] = time
        else: continue

# ------------------
# Get the time taken for each test from 'MultiQueueExecutor-core-results.txt'
# ------------------
multiQueue1coreResults = {}
multiQueue2coreResults = {}
multiQueue4coreResults = {}
multiQueue8coreResults = {}
multiQueue16coreResults = {}
multiQueue32coreResults = {}
with open('MultiQueueExecutor-core-results.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[0][84:89]
        if 'FAIL' in line: continue
        elif 'TIMEOUT' in line: time = 600_000
        else: time = int(parts[4])

        if "1core" in parts[1]:
            multiQueue1coreResults[problem_number] = time
        elif "2core" in parts[1]:
            multiQueue2coreResults[problem_number] = time
        elif "4core" in parts[1]:
            multiQueue4coreResults[problem_number] = time
        elif "8core" in parts[1]:
            multiQueue8coreResults[problem_number] = time
        elif "16core" in parts[1]:
            multiQueue16coreResults[problem_number] = time
        elif "Unbounded" in parts[1]:
            multiQueue32coreResults[problem_number] = time
        else:
            print("Error: unknown result")
            quit()

# -------------------
# Plot time difference between v0 and multiQueue1core for each test as a boxplot
# -------------------
EASY_TIME = 100
diffsEasy1 = [v0results[problem_number] - multiQueue1coreResults[problem_number] for problem_number in multiQueue1coreResults if v0results[problem_number] < EASY_TIME]

plt.boxplot([diffsEasy1])
plt.xlabel(f'median={np.round(np.median(diffsEasy1), 2)}')
plt.ylabel('v0 time - 1core MultiQueueExecutor time (ms)')
plt.title('Easy tests (<100ms): time difference between v0 and 1core MultiQueueExecutor')
plt.axhline(0, color='black', linestyle='--')
plt.show()

# -------------------
# Plot time difference between v0 and multiQueue32core for each test as a boxplot
# -------------------
diffsEasy32 = [v0results[problem_number] - multiQueue32coreResults[problem_number] for problem_number in multiQueue32coreResults if v0results[problem_number] < EASY_TIME]

plt.boxplot([diffsEasy32])
plt.xlabel(f'median={np.round(np.median(diffsEasy32), 2)}')
plt.ylabel('v0 time - 1core MultiQueueExecutor time (ms)')
plt.title('Easy tests (<100ms): time difference between v0 and 1core MultiQueueExecutor')
plt.axhline(0, color='black', linestyle='--')
plt.show()

# -------------------
# Plot v0 time / multiQueue1core time for each core-count for easy tests as scatter chart
# -------------------
EASY_RANGE = [0,1000]
MEDIUM_RANGE = [1000, 10_000]
HARD_RANGE = [10_000, 600_000]
def range_speedup(range, xlabel, ylabel, title):
    speedups = [[1, v0results[k] / multiQueue1coreResults[k]] for k in multiQueue1coreResults if range[0] < v0results[k] <= range[1]]
    speedups += [[2, v0results[k] / multiQueue2coreResults[k]] for k in multiQueue2coreResults if range[0] < v0results[k] <= range[1]]
    speedups += [[4, v0results[k] / multiQueue4coreResults[k]] for k in multiQueue4coreResults if range[0] < v0results[k] <= range[1]]
    speedups += [[8, v0results[k] / multiQueue8coreResults[k]] for k in multiQueue8coreResults if range[0] < v0results[k] <= range[1]]
    speedups += [[16, v0results[k] / multiQueue16coreResults[k]] for k in multiQueue16coreResults if range[0] < v0results[k] <= range[1]]
    speedups += [[32, v0results[k] / multiQueue32coreResults[k]] for k in multiQueue32coreResults if range[0] < v0results[k] <= range[1]]
    speedups = np.array(speedups)

    plt.scatter(speedups[:,0], speedups[:,1])
    xnew = np.linspace(min(speedups[:,0]), max(speedups[:,0]), 50)
    z = np.polyfit(np.log(speedups[:,0]), speedups[:,1], 1)
    f = np.poly1d(z)
    plt.plot(xnew, f(np.log(xnew)), 'r--')
    plt.xscale('log')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

range_speedup(EASY_RANGE, 'Core count', 'v0 time / MultiQueueExecutor time', 'Easy tests (<1000ms): v0 time / MultiQueueExecutor time for each core-count')
range_speedup(MEDIUM_RANGE, 'Core count', 'v0 time / MultiQueueExecutor time', 'Medium tests (1000-10000ms): v0 time / MultiQueueExecutor time for each core-count')
range_speedup(HARD_RANGE, 'Core count', 'v0 time / MultiQueueExecutor time', 'Hard tests (>10000ms): v0 time / MultiQueueExecutor time for each core-count')

# -------------------
# Get information about each test from 'ProblemInformation.txt'
# -------------------
# PREFIX,NUMBER,SUFFIX,ONTOLOGY,EMPTY,Expresivity (old),NOMINALS,HORN,,
empty = {}
expressivity = {}
nominals = {}
horn = {}
with open('ProblemInformation.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[1]
        empty[problem_number] = parts[4] == "true"
        expressivity[problem_number] = parts[5]
        nominals[problem_number] = parts[6] == "TRUE"
        horn[problem_number] = parts[7] == "TRUE"

# -------------------
# Plot v0 time / multiQueue1core time for each core-count for easy tests as multi-histogram
# -------------------
def plotMults(old_results, datas, labels, title, minn, maxx, num_bins, norm=False):
    mults = [{
        problem_number: old_results[problem_number] / data[problem_number]
        for problem_number in data
    } for data in datas]
    difs_bins = [i for i in np.linspace(minn-1, maxx+1, num_bins)]
    plt.hist([np.clip(list(mult.values()),difs_bins[0], difs_bins[-1]) for mult in mults],
             bins=difs_bins,
             label=labels,
             density=norm)
    plt.xlabel('New implementation time / v0 time')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title(title)
    plt.show()

plotMults(v0results, [multiQueue1coreResults, multiQueue16coreResults, multiQueue32coreResults],
          ['1core', '16core', '32core'],
          'Histogram of v0 time / MultiQueueExecutor time for each core-count',
          0, 5, 21)

# -------------------
# Plot v0 time / multiQueue1core time for 32-core for empty vs non-empty tests as histogram
# -------------------
plotMults(v0results,
          [{k: multiQueue32coreResults[k] for k in v0results if empty[k] and k in multiQueue32coreResults},
            {k: multiQueue32coreResults[k] for k in v0results if not empty[k] and k in multiQueue32coreResults}],
          ['Empty', 'Non-empty'],
          'Histogram of v0 time / MultiQueueExecutor time for empty vs non-empty tests (normalised)',
          0, 5, 21,
          norm=True)
# -------------------
# Plot v0 time / multiQueue1core time for 32-core for horn vs non-horn tests as histogram
# -------------------
plotMults(v0results,
          [{k: multiQueue32coreResults[k] for k in v0results if horn[k] and k in multiQueue32coreResults},
            {k: multiQueue32coreResults[k] for k in v0results if not horn[k] and k in multiQueue32coreResults}],
          ['Horn', 'Non-horn'],
          'Histogram of v0 time / MultiQueueExecutor time for horn vs non-horn tests (normalised)',
          0, 5, 21,
          norm=True)
# -------------------
# Plot v0 time / multiQueue1core time for 32-core for nominal vs non-nominal tests as histogram
# -------------------
plotMults(v0results,
          [{k: multiQueue32coreResults[k] for k in v0results if nominals[k] and k in multiQueue32coreResults},
            {k: multiQueue32coreResults[k] for k in v0results if not nominals[k] and k in multiQueue32coreResults}],
          ['Nominal', 'Non-nominal'],
          'Histogram of v0 time / MultiQueueExecutor time for nominal vs non-nominal tests (normalised)',
          0, 5, 21,
          norm=True)
# -------------------
# Plot v0 time / multiQueue1core time for 32-core for expressivity as histogram
# -------------------
expressivities = list(set(expressivity.values()))
plotMults(v0results,
          [{k: multiQueue32coreResults[k] for k in v0results if expressivity[k] == e and k in multiQueue32coreResults} for e in expressivities],
          expressivities,
          'Histogram of v0 time / MultiQueueExecutor time for each expressivity (normalised)',
          0, 5, 21,
          norm=True)

## TODO: !!! fix above chart to give more reasonable shape (maybe group some expressivities together)