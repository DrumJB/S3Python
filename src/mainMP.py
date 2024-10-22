import numpy as np
import multiprocessing as mp
import os
import readFile

data_folder = "./Programming/Projects/S3Python/data"

# get all objects in data folder
objs = os.listdir(data_folder)
# get all raw files in folder
raw_files = []
for o in objs:
    if o.split(".")[-1:][0] == 'raw':
        raw_files.append(data_folder+str("/")+str(o))

processes = []
for rf in raw_files:
    processes.append(mp.Process(target=readFile.readFile, args=(rf, )))

for p in processes:
    p.start()

for p in processes:
    p.join()

print("All data loaded in classes.")