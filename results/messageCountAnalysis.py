import matplotlib.pyplot as plt
import numpy as np

# -------------------
# Get number of messages sent for each test from 'MessageCountResults.txt'
# -------------------
selfMessageCount = {str(i).zfill(5): 0 for i in range(1, 800)}
otherMessageCount = {str(i).zfill(5): 0 for i in range(1, 800)}
with open('MessageCountResults.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[0][65:69]
         # Note: if the test timed out, the context count is 0. We will ignore these results in charts
         # Also note: Some tests failed - this is because they were removed from the test-set to reduce timeouts. They will also be ignored
        selfMessageCount[problem_number] = int(parts[7])
        otherMessageCount[problem_number] = int(parts[8])

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

# ------------------
# Get the time taken for each test from 'MultiQueueExecutor-core-results.txt'
# ------------------
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
        else:
            continue

# Filter out tests that timed out during the context count test (context count = 0)
noZeroesSelf = {k: v for k, v in selfMessageCount.items() if v != 0 and otherMessageCount[k] != 0}
noZeroesOther = {k: v for k, v in otherMessageCount.items() if v != 0 and selfMessageCount[k] != 0}

def plot_speedup(executorNoAkka, multiQueueExecutor, title, xlabel, ylabel, log=True, lobf=True):
    plt.scatter(executorNoAkka[:,0], executorNoAkka[:,1], label="ExecutorNoAkka", color='b')
    plt.scatter(multiQueueExecutor[:,0], multiQueueExecutor[:,1], label="MultiQueueExecutor", color='r')

    if log:
        # Lines of best fit
        xnew = np.linspace(min(executorNoAkka[:,0]), max(executorNoAkka[:,0]), 50)
        # - ExecutorNoAkka
        z = np.polyfit(np.log(executorNoAkka[:,0]), executorNoAkka[:,1], 1)
        f = np.poly1d(z)
        plt.plot(xnew, f(np.log(xnew)), 'b--')
        # - MultiQueueExecutor
        z = np.polyfit(np.log(multiQueueExecutor[:,0]), multiQueueExecutor[:,1], 1)
        f = np.poly1d(z)
        plt.plot(xnew, f(np.log(xnew)), 'r--')
        
        plt.xscale('log')
    elif lobf:
        # Lines of best fit
        xnew = np.linspace(min(executorNoAkka[:,0]), max(executorNoAkka[:,0]), 50)
        # - ExecutorNoAkka
        z = np.polyfit(executorNoAkka[:,0], executorNoAkka[:,1], 1)
        f = np.poly1d(z)
        plt.plot(xnew, f(xnew), 'b--')
        # - MultiQueueExecutor
        z = np.polyfit(multiQueueExecutor[:,0], multiQueueExecutor[:,1], 1)
        f = np.poly1d(z)
        plt.plot(xnew, f(xnew), 'r--')
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.title(title)
    plt.show()

def plot_speedup_single(data, title, xlabel, ylabel):
    plt.scatter(data[:,0], data[:,1], label="MultiQueueExecutor", color='r')
    
    plt.xscale('log')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.title(title)
    plt.show()


# -------------------
# Plot scatter graph of speedup (v0 time / ExecutorNoAkka time) (y-axis) vs number of self-messages (x-axis)
# On same axis, plot speedup (v0 time / MultiQueueExecutor time) (y-axis) vs number of self-messages (x-axis)
# -------------------
executorNoAkkaSpeedup = np.array([[int(noZeroesSelf[k]), v0results[k] / executorNoAkkaResults[k]] for k in noZeroesSelf])
multiQueueExecutorSpeedup = np.array([[int(noZeroesSelf[k]), v0results[k] / multiQueueExecutorResults[k]] for k in noZeroesSelf])
plot_speedup(executorNoAkkaSpeedup,
             multiQueueExecutorSpeedup,
             "Speedup vs Number of self-messages",
             "Number of self-messages",
             "Speedup (v0 time / new implementation time)")


# -------------------
# Plot scatter graph of speedup (ExecutorNoAkka-1core time / ExecutorNoAkka time) (y-axis) vs number of self-messages (x-axis)
# On same axis, plot speedup (MultiQueueExecutor-1core time / MultiQueueExecutor time) (y-axis) vs number of self-messages (x-axis)
# -------------------
multiQueue1coreSpeedup = np.array([[int(noZeroesSelf[k]), multiQueue1coreResults[k] / multiQueue32coreResults[k]] for k in noZeroesSelf])
plot_speedup_single(multiQueue1coreSpeedup,
                    "Speedup vs Number of self-messages",
                    "Number of self-messages",
                    "Speedup (MultiQueueExecutor-32core time / MultiQueueExecutor-1core time)")


# -------------------
# Plot scatter graph of speedup (v0 time / ExecutorNoAkka time) (y-axis) vs number of other-messages (x-axis)
# On same axis, plot speedup (v0 time / MultiQueueExecutor time) (y-axis) vs number of other-messages (x-axis)
# -------------------
executorNoAkkaSpeedupOther = np.array([[int(noZeroesOther[k]), v0results[k] / executorNoAkkaResults[k]] for k in noZeroesOther])
multiQueueExecutorSpeedupOther = np.array([[int(noZeroesOther[k]), v0results[k] / multiQueueExecutorResults[k]] for k in noZeroesOther])
plot_speedup(executorNoAkkaSpeedupOther,
             multiQueueExecutorSpeedupOther,
             "Speedup vs Number of other-messages",
             "Number of other-messages",
             "Speedup (v0 time / new implementation time)")


# -------------------
# Plot scatter graph of speedup (ExecutorNoAkka-1core time / ExecutorNoAkka time) (y-axis) vs number of other-messages (x-axis)
# On same axis, plot speedup (MultiQueueExecutor-1core time / MultiQueueExecutor time) (y-axis) vs number of other-messages (x-axis)
# -------------------
multiQueue1coreSpeedupOther = np.array([[int(noZeroesOther[k]), multiQueue1coreResults[k] / multiQueue32coreResults[k]] for k in noZeroesOther])
plot_speedup_single(multiQueue1coreSpeedupOther,
                    "Speedup vs Number of other-messages",
                    "Number of other-messages",
                    "Speedup (MultiQueueExecutor-32core time / MultiQueueExecutor-1core time)")


# -------------------
# Plot scatter graph of speedup (v0 time / ExecutorNoAkka time) (y-axis) vs number of other-messages / self-messages (x-axis)
# On same axis, plot speedup (v0 time / MultiQueueExecutor time) (y-axis) vs number of other-messages / self-messages (x-axis)
# -------------------
# We filter out tests where the ratio of other-messages to self-messages is greater than 1 since these are outliers
# We filter to only include tests where the new implementation time is greater than 3000ms since those are the ones we care about speeding up most
executorNoAkkaSpeedupRatio = np.array([[int(noZeroesOther[k]) / float(noZeroesSelf[k]), v0results[k] / executorNoAkkaResults[k]] for k in noZeroesOther if executorNoAkkaResults[k] >= 3000 and int(noZeroesOther[k]) / float(noZeroesSelf[k]) <= 1])
multiQueueExecutorSpeedupRatio = np.array([[int(noZeroesOther[k]) / float(noZeroesSelf[k]), v0results[k] / multiQueueExecutorResults[k]] for k in noZeroesOther if multiQueueExecutorResults[k] >= 3000 and int(noZeroesOther[k]) / float(noZeroesSelf[k]) <= 1])
plot_speedup(executorNoAkkaSpeedupRatio,
             multiQueueExecutorSpeedupRatio,
             "Speedup vs ratio other-messages : self-messages",
             "Ratio other-messages : self-messages",
             "Speedup (v0 time / new implementation time)",
             log=False,
             lobf=False)

# -------------------
# Plot scatter graph of speedup (ExecutorNoAkka-1core time / ExecutorNoAkka time) (y-axis) vs number of other-messages / self-messages (x-axis)
# On same axis, plot speedup (MultiQueueExecutor-1core time / MultiQueueExecutor time) (y-axis) vs number of other-messages / self-messages (x-axis)
# -------------------
multiQueue1coreSpeedupRatio = np.array([[int(noZeroesOther[k]) / float(noZeroesSelf[k]), multiQueue1coreResults[k] / multiQueue32coreResults[k]] for k in noZeroesOther if multiQueue32coreResults[k] >= 3000 and int(noZeroesOther[k]) / float(noZeroesSelf[k]) <= 1])
plot_speedup_single(multiQueue1coreSpeedupRatio,
                    "Speedup vs ratio other-messages : self-messages",
                    "Ratio other-messages : self-messages",
                    "Speedup (MultiQueueExecutor-32core time / MultiQueueExecutor-1core time)")