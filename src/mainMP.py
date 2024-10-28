# library import
import numpy as np
import multiprocessing as mp
import os
import readFile
import datetime

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


# pooling (the method is undestandably explained e.g. here: https://www.geeksforgeeks.org/synchronization-pooling-processes-python/)

pool = mp.Pool()    # Pool object

all_events = pool.map(readFile.readFile, raw_files)

# print out
print("All data loaded in classes.")

# end log
print(f"END: {datetime.datetime.now()}")