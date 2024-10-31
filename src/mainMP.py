# library import
import numpy as np
import multiprocessing as mp
import os
import datetime
import psutil as pu
import sys
import json

import readFile
import eventEnergy

####################
#  INITIALIZATION  #
####################


# start log
print(f"START: {datetime.datetime.now()}")

# loading json settings from file given in argument when run
# program now launched using e.g. 'python ./src/mainMP ./settings.json'
json_file = sys.argv[1]
with open(json_file, "rb") as settings_file:
    settings = json.load(settings_file)

# debug on n files only
debug_mode = settings["debug"]["debug_mode"]
debug_n_files = settings["debug"]["debug_n_files"]
if debug_mode: print(f"DEBUG MODE: activated, debug_n_files={debug_n_files}")

# data folder path
data_folder = settings["main"]["data_folder"]    

# maximum RAM usage
max_RAM_usage = settings["run_config"]["max_RAM_usage"]

####################
#       MAIN       #
####################

## LOADING

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

## PROCESSING FUNCTION

# function for processing one file, called in Pool
def processFile(file_name):
    done = False
    while not done:     # try to run the job if not done
        if pu.virtual_memory()[2]/100 < max_RAM_usage:
            events = readFile.readFile(file_name)
            eventEnergy.eventEnergy(events)
            done=True

## MULTIPROCESSING - POOLING

# pooling (the method is undestandably explained e.g. here: https://www.geeksforgeeks.org/synchronization-pooling-processes-python/)
cpu_c = mp.cpu_count()
if mp.cpu_count() > 2:
    cpu_c += -2

pool = mp.Pool(cpu_c)    # Pool object
chunk_size = len(raw_files) // cpu_c   # how many files each will be worker assigned
if chunk_size == 0: chunk_size=1    # not zero if the cpu number is larger

all_events = pool.imap_unordered(processFile, raw_files, chunksize=chunk_size) # returns iterator

pool.close()
pool.join()

## END

# end log
print(f"END: {datetime.datetime.now()}")