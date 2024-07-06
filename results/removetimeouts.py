# Read timeouts.txt - a file containing the 5 digit string forms of tests that timed out using the original reasoner
# Copy all tests that did not time out to a new directory to create a smaller test set for quicker testing

import matplotlib.pyplot as plt
import numpy as np

with open('timeouts.txt', 'r') as f:
    lines = f.readlines()

timeouts = set()
for line in lines:
    timeouts.add(str(line[:5]))

#make list of 5 digit string forms of numbers 00001-00799
nottimeouts = set([str(i).zfill(5) for i in range(1, 800)])

filenamestocopy = [x + ".owl.DL.owl.SROIQ.owl" for x in nottimeouts if x not in timeouts]


# copy all files in /home/pigeon/Downloads/msc/MSc-Project/testing/data/oxfordcorpus-fixed-dl-SROIQ such that the filename is in filenamestocopy to /home/pigeon/Downloads/msc/MSc-Project/testing/data/no-timeouts
import shutil
for filename in filenamestocopy:
    shutil.copy("/home/pigeon/Downloads/msc/MSc-Project/testing/data/oxfordcorpus-fixed-dl-SROIQ/" + filename, "/home/pigeon/Downloads/msc/MSc-Project/testing/data/no-timeouts/" + filename)


print(sorted(filenamestocopy))

print(timeouts)