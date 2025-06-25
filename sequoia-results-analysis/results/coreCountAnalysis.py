import matplotlib.pyplot as plt
import numpy as np

# -------------------
# Get time taken for each test from 'v0-ExecutorNoAkka-MultiQueueExecutor-32core-results.txt'
# -------------------
v0results = {}
extraMultiq = {}
with open('v0-ExecutorNoAkka-MultiQueueExecutor-32core-results.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[0][84:89]
        if 'TIMEOUT' in line: time = 600_000
        else: time = int(parts[4])

        if "OLD" in parts[1]:
            v0results[problem_number] = time
        elif "FUNKY" in parts[1]:
            extraMultiq[problem_number] = time
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

plt.hist([diffsEasy1], bins=30)
print(f'median={np.round(np.median(diffsEasy1), 2)}')
plt.xlabel('CSO time - 1core MultiQueueExecutor time (ms)')
plt.ylabel('Frequency')
plt.title('Time difference histogram (very easy problems, <100ms)')
plt.axhline(0, color='black', linestyle='--')
plt.show()

# -------------------
# Plot time difference between v0 and multiQueue32core for each test as a boxplot
# -------------------
diffsEasy32 = [v0results[problem_number] - multiQueue32coreResults[problem_number] for problem_number in multiQueue32coreResults if v0results[problem_number] < EASY_TIME]

plt.hist([diffsEasy32], bins=30)
print(f'median={np.round(np.median(diffsEasy32), 2)}')
plt.xlabel('CSO time - 32core MultiQueueExecutor time (ms)')
plt.ylabel('Frequency')
plt.title('Time difference histogram (very easy problems, <100ms)')
plt.axhline(0, color='black', linestyle='--')
plt.show()

# -------------------
# Plot v0 time / multiQueue1core time for each core-count for easy tests as scatter chart
# -------------------
EASY_RANGE = [0,1000]
MEDIUM_RANGE = [1000, 10_000]
HARD_RANGE = [10_000, 599_999]
def range_speedup(range, xlabel, ylabel, title):
    speedups = [[1, v0results[k] / multiQueue1coreResults[k]] for k in multiQueue1coreResults if range[0] < v0results[k] <= range[1]]
    speedups += [[2, v0results[k] / multiQueue2coreResults[k]] for k in multiQueue2coreResults if range[0] < v0results[k] <= range[1]]
    speedups += [[4, v0results[k] / multiQueue4coreResults[k]] for k in multiQueue4coreResults if range[0] < v0results[k] <= range[1]]
    speedups += [[8, v0results[k] / multiQueue8coreResults[k]] for k in multiQueue8coreResults if range[0] < v0results[k] <= range[1]]
    speedups += [[16, v0results[k] / multiQueue16coreResults[k]] for k in multiQueue16coreResults if range[0] < v0results[k] <= range[1]]
    # speedups += [[32, v0results[k] / multiQueue32coreResults[k]] for k in multiQueue32coreResults if range[0] < v0results[k] <= range[1]]
    speedups = np.array(speedups)

    plt.scatter(speedups[:,0], speedups[:,1])
    xnew = np.linspace(min(speedups[:,0]), max(speedups[:,0]), 50)
    z = np.polyfit(np.log(speedups[:,0]), speedups[:,1], 1)
    f = np.poly1d(z)
    print(f"y = {z[0]}*log(x) + {z[1]}")
    plt.plot(xnew, f(np.log(xnew)), 'r--')
    plt.xscale('log')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


range_speedup(EASY_RANGE, 'Core count', 'CSO time / MultiQueueExecutor time', 'CSO time / MultiQueueExecutor (easy problems)')
range_speedup(MEDIUM_RANGE, 'Core count', 'CSO time / MultiQueueExecutor time', 'CSO time / MultiQueueExecutor (medium problems)')
range_speedup(HARD_RANGE, 'Core count', 'CSO time / MultiQueueExecutor time', 'CSO time / MultiQueueExecutor (hard problems)')

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
def plotMults(old_results, datas, labels, title, minn, maxx, num_bins, norm=False, color=None, hard=False):
    if hard:
        mults = [{
            problem_number: old_results[problem_number] / data[problem_number]
            for problem_number in data if HARD_RANGE[0] < old_results[problem_number] <= HARD_RANGE[1]
        } for data in datas]
    else:
        mults = [{
            problem_number: old_results[problem_number] / data[problem_number]
            for problem_number in data
        } for data in datas]
    difs_bins = [i for i in np.linspace(minn-1, maxx+1, num_bins)]
    plt.hist([np.clip(list(mult.values()),difs_bins[0], difs_bins[-1]) for mult in mults],
             bins=difs_bins,
             label=labels,
             color=color,
             density=norm)
    plt.xlabel('CSO time / MultiQueueExecutor time')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title(title)
    plt.show()

plotMults(v0results, [multiQueue1coreResults, multiQueue2coreResults, multiQueue4coreResults, multiQueue8coreResults, multiQueue16coreResults, multiQueue32coreResults],
          ['1core', '2core', '4core', '8core', '16core', '32core'],
          'Speedup histogram per core-count (hard problems)',
          0, 5, 11, color=['blue', 'purple', 'green', 'brown', 'orange', 'red'], hard=True)

nozerov0results = {k: v0results[k] for k in v0results if v0results[k] < 600_000}
nozeromultiQueue32coreResults = {k: multiQueue32coreResults[k] for k in multiQueue32coreResults if k in v0results and v0results[k] < 600_000}

# -------------------
# Plot v0 time / multiQueue1core time for 32-core for empty vs non-empty tests as histogram
# -------------------
plotMults(nozerov0results,
          [{k: nozeromultiQueue32coreResults[k] for k in nozerov0results if empty[k] and k in nozeromultiQueue32coreResults},
            {k: nozeromultiQueue32coreResults[k] for k in nozerov0results if not empty[k] and k in nozeromultiQueue32coreResults}],
          ['Empty', 'Non-empty'],
          'Speedup histogram for empty vs non-empty (normalised)',
          0, 5, 21,
          norm=True)
print(f"Empty average speedup: {np.mean([nozerov0results[k] / nozeromultiQueue32coreResults[k] for k in nozeromultiQueue32coreResults if empty[k]])}")
print(f"Non-empty average speedup: {np.mean([nozerov0results[k] / nozeromultiQueue32coreResults[k] for k in nozeromultiQueue32coreResults if not empty[k]])}")

# -------------------
# Plot v0 time / multiQueue1core time for 32-core for horn vs non-horn tests as histogram
# -------------------
plotMults(nozerov0results,
          [{k: nozeromultiQueue32coreResults[k] for k in nozerov0results if horn[k] and k in nozeromultiQueue32coreResults and nozerov0results[k] <= 599_999},
            {k: nozeromultiQueue32coreResults[k] for k in nozerov0results if not horn[k] and k in nozeromultiQueue32coreResults and nozerov0results[k] <= 599_999}],
          ['Horn', 'Non-horn'],
          'Speedup histogram for horn vs non-horn (normalised)',
          0, 5, 21,
          norm=True)
print(f"Horn average speedup: {np.mean([nozerov0results[k] / nozeromultiQueue32coreResults[k] for k in nozeromultiQueue32coreResults if horn[k]])}")
print(f"Non-horn average speedup: {np.mean([nozerov0results[k] / nozeromultiQueue32coreResults[k] for k in nozeromultiQueue32coreResults if not horn[k]])}")

print(f"Average hard Horn speedup: {np.mean([nozerov0results[k] / nozeromultiQueue32coreResults[k] for k in nozeromultiQueue32coreResults if horn[k] and nozerov0results[k] > 10_000])}")
print(f"Average hard Non-horn speedup: {np.mean([nozerov0results[k] / nozeromultiQueue32coreResults[k] for k in nozeromultiQueue32coreResults if not horn[k] and nozerov0results[k] > 10_000])}")

# -------------------
# Plot v0 time / multiQueue1core time for 32-core for nominal vs non-nominal tests as histogram
# -------------------
plotMults(nozerov0results,
          [{k: nozeromultiQueue32coreResults[k] for k in nozerov0results if nominals[k] and k in nozeromultiQueue32coreResults},
            {k: nozeromultiQueue32coreResults[k] for k in nozerov0results if not nominals[k] and k in nozeromultiQueue32coreResults}],
          ['Nominal', 'Non-nominal'],
          'Speedup histogram for nominal vs non-nominal (normalised)',
          0, 5, 21,
          norm=True)
print(f"Nominal average speedup: {np.mean([nozerov0results[k] / nozeromultiQueue32coreResults[k] for k in nozeromultiQueue32coreResults if nominals[k]])}")
print(f"Non-nominal average speedup: {np.mean([nozerov0results[k] / nozeromultiQueue32coreResults[k] for k in nozeromultiQueue32coreResults if not nominals[k]])}")
# # -------------------
# # Plot v0 time / multiQueue1core time for 32-core for expressivity as histogram
# # -------------------
# expressivities = list(set(expressivity.values()))
# plotMults(nozerov0results,
#           [{k: nozeromultiQueue32coreResults[k] for k in nozerov0results if expressivity[k] == e and k in nozeromultiQueue32coreResults} for e in expressivities],
#           expressivities,
#           'Histogram of v0 time / MultiQueueExecutor time for each expressivity (normalised)',
#           0, 5, 21,
#           norm=True)

# ## TODO: !!! fix above chart to give more reasonable shape (maybe group some expressivities together)

# -------------------
# Plot median v0 time / multiQueue1core time for 32-core for each expressivity as bar chart
# -------------------
expressivities = sorted(list(set(expressivity.values()))) 
medians = np.array([[e, float(np.median([nozerov0results[k] / nozeromultiQueue32coreResults[k] for k in nozeromultiQueue32coreResults if expressivity[k] == e]))] for e in expressivities])
# print(medians)
plt.bar(medians[:,0], [float(x) for x in medians[:,1]])
plt.xticks(rotation=90)
plt.show()

# -------------------
# Plot v0 time / multiQueue32core time against v0 time for each test as scatter chart
# -------------------
speedups = np.array([[v0results[k], v0results[k] / extraMultiq[k]] for k in extraMultiq if v0results[k] < 600_000])
# lobf
xnew = np.linspace(min(speedups[:,0]), max(speedups[:,0]), 50)
z = np.polyfit(np.log(speedups[:,0]), np.log(speedups[:,1]), 1)
f = np.poly1d(z)
print(f"y = {z[0]}*x + {z[1]}")
plt.plot(xnew, np.exp(f(np.log(xnew))), 'r--')
plt.scatter(speedups[:,0], speedups[:,1], label='extra')
plt.xlabel('CSO time (ms)')
plt.ylabel('CSO time / 32core MultiQueueExecutor time')
plt.title('Speedup vs CSO time scatter graph')
plt.xscale('log')
plt.yscale('log')
plt.show()

# Print ordered speedups so best and worst hard-tests can be examined
ordered_speedups = sorted([[k, v0results[k] / multiQueue32coreResults[k]] for k in multiQueue32coreResults if v0results[k] > 10_000], key=lambda x: x[1])
# print(ordered_speedups)
# 00786 is only slow because of a single bad test run
# Some are timeouts - can only have speedup of 1.0
# 00008 - 4core and 2core have a >1.0 speedup but 32core has <1.0 speedup (probably either due to other processes running / bad test)
# either way, 00008 is not particularly parallelisable