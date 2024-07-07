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


# -------------------
# Plot scatter graph of time taken (v0)
# Plot scatter graph of time taken (ExecutorNoAkka)
# Plot scatter graph of time taken (MultiQueueExecutor)
# -------------------

# TODO: !!! plot this

plt.plot([0],[0])
plt.show()



# -------------------
# Plot histogram bell-curve of speedup (v0 time - ExecutorNoAkka time)
# Plot histogram bell-curve of speedup (v0 time - MultiQueueExecutor time)
# -------------------
differencesExecutorNoAkka = {
    problem_number: v0results[problem_number] - executorNoAkkaResults[problem_number]
    for problem_number in executorNoAkkaResults
}
differencesMultiQueueExecutor = {
    problem_number: v0results[problem_number] - multiQueueExecutorResults[problem_number]
    for problem_number in multiQueueExecutorResults
}
difs_bins = [i for i in range(-10_000, 100_000, 1000)]
plt.hist([np.clip(list(differencesExecutorNoAkka.values()), difs_bins[0], difs_bins[-1]), np.clip(list(differencesMultiQueueExecutor.values()), difs_bins[0], difs_bins[-1])],
         bins=difs_bins,
         label=["ExecutorNoAkka", "MultiQueueExecutor"])
plt.xlabel('New time - old time (ms)')
plt.ylabel('Frequency')
plt.legend()
plt.title('Absolute speedup histogram')
plt.show()

# -------------------
# On the same chart, plot histogram bell-curve of speedup (v0 time - MultiQueueExecutor time)
# -------------------
multsExecutorNoAkka = {
    problem_number: v0results[problem_number] / executorNoAkkaResults[problem_number]
    for problem_number in executorNoAkkaResults
}
multsMultiQueueExecutor = {
    problem_number: v0results[problem_number] / multiQueueExecutorResults[problem_number]
    for problem_number in multiQueueExecutorResults
}

# TODO: !!! plot this

plt.plot([0],[0])
plt.show()

# Plot the multiples distribution
# mult_bins = [i/10 for i in range(0, 50)]
# plt.hist(np.clip(list(mults.values()), mult_bins[0], mult_bins[-1]), bins=mult_bins)
# plt.xlabel('Old time / new time (ms)')
# plt.ylabel('Frequency')
# plt.show()
# plt.hist(np.clip(list(differencesMultiQueueExecutor.values()), difs_bins[0], difs_bins[-1]), bins=difs_bins, label="MultiQueueExecutor", alpha=0.5)
# plt.xlabel('New time - old time (ms)')
# plt.ylabel('Frequency')




# -------------------
# Plot histogram bell-curve of speedup (v0 time - ExecutorNoAkka time)
# -------------------

# -------------------
# On same chart, plot histogram bell-curve of speedup (v0 time - MultiQueueExecutor time)
# -------------------