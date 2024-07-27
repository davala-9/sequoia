import matplotlib.pyplot as plt
import numpy as np

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

print("number of results <10min for multiQ", len([k for k,v in multiQueueExecutorResults.items() if v < 600_000]))
print("number of results <10min for noakka", len([k for k,v in executorNoAkkaResults.items() if v < 600_000]))
print("number of results <10min for v0", len([k for k,v in v0results.items() if v < 600_000]))

# -------------------
# Plot histogram of time taken (v0)
# Plot histogram of time taken (ExecutorNoAkka)
# Plot histogram of time taken (MultiQueueExecutor)
# -------------------

plt.hist([np.clip(list(v0results.values()), 0, 600_000), np.clip(list(executorNoAkkaResults.values()), 0, 600_000), np.clip(list(multiQueueExecutorResults.values()), 0, 600_000)],
         bins=[i for i in range(0, 600_001, 10_000)],
         label=["CSO", "SingleQueueExecutor", "MultiQueueExecutor"],
         color=['b', 'orange', 'g'])

plt.xlabel('Time taken (ms)')
plt.ylabel('Frequency')
plt.legend()
plt.title('Histogram of time taken for each model')
plt.show()



# -------------------
# Plot histogram bell-curve of speedup (v0 time - ExecutorNoAkka time)
# Plot histogram bell-curve of speedup (v0 time - MultiQueueExecutor time)
# -------------------
EASY_TIME = 1000
MEDIUM_TIME = 10_000
def plotDifferences(old_results, noakka, multi, title, minn, maxx, step):
    differences1 = {
        problem_number: old_results[problem_number] - noakka[problem_number]
        for problem_number in old_results
    }
    differences2 = {
        problem_number: old_results[problem_number] - multi[problem_number]
        for problem_number in old_results
    }
    difs_bins = [i for i in range(minn-1, maxx+1, step)]
    plt.hist([np.clip(list(differences1.values()),difs_bins[0], difs_bins[-1]), np.clip(list(differences2.values()), difs_bins[0], difs_bins[-1])],
             bins=difs_bins,
             label=["SingleQueueExecutor", "MultiQueueExecutor"])
    plt.xlabel('New implementation time - CSO time (ms)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title(title)
    plt.show()

plotDifferences({k: v for k,v in v0results.items() if v < EASY_TIME},
                executorNoAkkaResults,
                multiQueueExecutorResults,
                'Time difference histogram (easy problems)',
                -1_000,
                1_000,
                100)
plotDifferences({k: v for k,v in v0results.items() if v >= EASY_TIME and v < MEDIUM_TIME},
                executorNoAkkaResults,
                multiQueueExecutorResults,
                'Time difference histogram (medium problems)',
                -10_000,
                10_000,
                1_000)
plotDifferences({k: v for k,v in v0results.items() if v >= MEDIUM_TIME},
                executorNoAkkaResults,
                multiQueueExecutorResults,
                'Time difference histogram (hard problems)',
                -100_000,
                100_000,
                10_000)

# -------------------
# Plot histogram bell-curve of speedup (v0 time / MultiQueueExecutor time)
# Plot histogram bell-curve of speedup (v0 time / ExecutorNoAkka time)
# -------------------
def plotMults(old_results, noakka, multi, title, minn, maxx, num_bins):
    mults1 = {
        problem_number: old_results[problem_number] / noakka[problem_number]
        for problem_number in old_results if v0results[problem_number] < 600_000
    }
    mults2 = {
        problem_number: old_results[problem_number] / multi[problem_number]
        for problem_number in old_results if v0results[problem_number] < 600_000
    }
    difs_bins = [i for i in np.linspace(minn-1, maxx+1, num_bins)]
    plt.hist([np.clip(list(mults1.values()),difs_bins[0], difs_bins[-1]), np.clip(list(mults2.values()), difs_bins[0], difs_bins[-1])],
             bins=difs_bins,
             label=["SingleQueueExecutor", "MultiQueueExecutor"])
    plt.xlabel('CSO time / New implementation time')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title(title)
    plt.show()

plotMults({k: v for k,v in v0results.items() if v < EASY_TIME},
          executorNoAkkaResults,
          multiQueueExecutorResults,
          'Speedup histogram (easy problems)',
          0,
          5,
          21)
plotMults({k: v for k,v in v0results.items() if v >= EASY_TIME and v < MEDIUM_TIME},
          executorNoAkkaResults,
          multiQueueExecutorResults,
          'Speedup histogram (medium problems)',
          0,
          5,
          21)
plotMults({k: v for k,v in v0results.items() if v >= MEDIUM_TIME},
          executorNoAkkaResults,
          multiQueueExecutorResults,
          'Speedup histogram (hard problems)',
          0,
          5,
          21)

print("Average speedup for easy problems (singleq)", np.mean([v for k,v in {k: v0results[k] / executorNoAkkaResults[k] for k in v0results if v0results[k] < EASY_TIME}.items() if v0results[k] < 600_000]))
print("Average speedup for medium problems (singleq)", np.mean([v for k,v in {k: v0results[k] / executorNoAkkaResults[k] for k in v0results if v0results[k] >= EASY_TIME and v0results[k] < MEDIUM_TIME}.items() if v0results[k] < 600_000]))
print("Average speedup for hard problems (singleq)", np.mean([v for k,v in {k: v0results[k] / executorNoAkkaResults[k] for k in v0results if v0results[k] >= MEDIUM_TIME}.items() if v0results[k] < 600_000]))

print("Average speedup for easy problems", np.mean([v for k,v in {k: v0results[k] / multiQueueExecutorResults[k] for k in v0results if v0results[k] < EASY_TIME}.items() if v0results[k] < 600_000]))
print("Average speedup for medium problems", np.mean([v for k,v in {k: v0results[k] / multiQueueExecutorResults[k] for k in v0results if v0results[k] >= EASY_TIME and v0results[k] < MEDIUM_TIME}.items() if v0results[k] < 600_000]))
print("Average speedup for hard problems", np.mean([v for k,v in {k: v0results[k] / multiQueueExecutorResults[k] for k in v0results if v0results[k] >= MEDIUM_TIME}.items() if v0results[k] < 600_000]))