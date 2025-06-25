import matplotlib.pyplot as plt
import numpy as np

executorNoAkkaResults = {}
with open('v0-ExecutorNoAkka-MultiQueueExecutor-32core-results.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[0][85:89]
        if 'TIMEOUT' in line: time = 600_000
        else: time = int(parts[4])

        if "EXECUTORnoakkasequoia" in parts[1]:
            executorNoAkkaResults[problem_number] = time

akkaResults = {}
olds = {}
with open('AkkaSequoiaResults.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[0][74:78]
        if 'TIMEOUT' in line: time = 600_000
        elif 'SUCCESS' in line: time = int(parts[4])
        else: continue

        if "AKKAsequoia" in parts[1]:
            akkaResults[problem_number] = time
        elif "OLD" in parts[1]:
            olds[problem_number] = time


mults = { problem_number: akkaResults[problem_number] / executorNoAkkaResults[problem_number] for problem_number in akkaResults }
# bins = [i for i in range(-10_000, 50_000, 1000)]
bins = [i/10 for i in range(0, 50)]
plt.hist(np.clip(list(mults.values()), bins[0], bins[-1]), bins=bins)
# plt.hist(mults.values())
plt.title('ExecutorSequoia vs AkkaSequoia. Higher number = ExecutorSequoia is faster')
plt.xlabel('AkkaSequoia time / ExecutorSequoia time, median = ' + str(np.median(list(mults.values()))))
plt.ylabel('Frequency')
plt.show()
print(max(mults.values()))
print(max(akkaResults.values()))
print(len(akkaResults))
x = { problem_number: olds[problem_number] / akkaResults[problem_number] for problem_number in akkaResults }
print(f"Median akka speedup vs cso: {np.median(list(x.values()))}")


multsOld = { problem_number: olds[problem_number] / executorNoAkkaResults[problem_number] for problem_number in akkaResults }
bins = [i/10 for i in range(0, 50)]
plt.hist(np.clip(list(multsOld.values()), bins[0], bins[-1]), bins=bins)
plt.title('ExecutorSequoia vs CSOSequoia. Higher number = ExecutorSequoia is faster')
plt.xlabel('CSOSequoia time / ExecutorSequoia time, median = ' + str(np.median(list(multsOld.values()))))
plt.ylabel('Frequency')
plt.show()

hashes = {}
hashesNew = {}
with open('v0-ExecutorNoAkka-MultiQueueExecutor-32core-results.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(",")
        problem_number = parts[0][85:89]
        if 'SUCCESS' in line: h = line[3]
        if 'OLD' in line: hashes[problem_number] = h
        elif 'EXECUTORnoakkasequoia' in line: hashesNew[problem_number] = h

# print("----")
# for problem_number in hashes:
#     if hashes[problem_number] != hashesNew[problem_number]:
#         print(problem_number)
#         print(hashes[problem_number])
#         print(hashesNew[problem_number])
#         print()
# print("----")
# print(len(hashes))
# print(len(hashesNew))