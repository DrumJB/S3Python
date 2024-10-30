# library import
import numpy as np
import multiprocessing as mp
import os
import readFile
import datetime

# debug on n files only
debug = True
debug_n_files = 6

# start log
print(f"START: {datetime.datetime.now()}")

data_folder = "./Programming/Projects/S3Python/data"    # data folder path

# get all objects in data folder
objs = os.listdir(data_folder)
# get all raw files in folder
raw_files = []
for o in objs:
    if o.split(".")[-1:][0] == 'raw':
        raw_files.append(data_folder+str("/")+str(o))   
        # append raw file to file names list with full path

# set number of files to load equal to debug_n_files if debug
raw_files = raw_files[:debug_n_files]

# pooling (the method is undestandably explained e.g. here: https://www.geeksforgeeks.org/synchronization-pooling-processes-python/)
cpu_c = mp.cpu_count()
if mp.cpu_count() > 2:
    cpu_c += -2

pool = mp.Pool(cpu_c)    # Pool object
chunk_size = len(raw_files) // cpu_c   # how many files each will be worker assigned
if chunk_size == 0: chunk_size=1    # not zero if the cpu number is larger

all_events = pool.imap_unordered(readFile.readFile, raw_files, chunksize=chunk_size) # returns iterator

pool.close()
pool.join()

# print out
print("All data loaded in classes.")

# end log
print(f"END: {datetime.datetime.now()}")