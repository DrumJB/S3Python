# library import
import numpy as np
import multiprocessing as mp
import os
import readFile

data_folder = "./Programming/Projects/S3Python/data"    # data folder path

# get all objects in data folder
objs = os.listdir(data_folder)
# get all raw files in folder
raw_files = []
for o in objs:
    if o.split(".")[-1:][0] == 'raw':
        raw_files.append(data_folder+str("/")+str(o))   
        # append raw file to file names list with full path

processes = []  # list of all processes
for rf in raw_files:
    processes.append(mp.Process(target=readFile.readFile, args=(rf, )))
    # set up all processes

for p in processes:
    # start all processes
    p.start()

for p in processes:
    # wait until all processes end
    p.join()

# print out
print("All data loaded in classes.")