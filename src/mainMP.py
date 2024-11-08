# library import
import numpy as np
import pandas as pd
import multiprocessing as mp
import os
import datetime
import psutil as pu
import sys
import json
import time

import readFile
import eventEnergy
import energyCalibration

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
# export to CSV
export_CSV = settings["main"]["export_events_to_CSV"]
CSV_name = settings["main"]["CSV_name"] + ".csv"
# calibrate
energy_calibration = settings['main']['energy_calibration']

# processFile timeout
timeout = settings["run_config"]["processFile_timeout"]

# maximum RAM usage
max_RAM_usage = settings["run_config"]["max_RAM_usage"]
POSIX_drop_cache = settings["run_config"]["POSIX_drop_cache"]
POSIX_drop_cache_continuously = settings["run_config"]["POSIX_drop_cache_continuously"]

# clear RAM cache if run on POSIX system
if os.name == 'posix' and POSIX_drop_cache:
    os.system("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
    print("INFO: RAM cache cleared.")

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
if debug_mode: raw_files = raw_files[:debug_n_files]

## PROCESSING FUNCTION

# function for processing one file, called in Pool
def processFile(file_name):
    done = False
    energies = []
    while not done:     # try to run the job if not done
        if pu.virtual_memory()[2]/100 < max_RAM_usage:
            events = readFile.readFile(file_name)
            energies = eventEnergy.eventsEnergy(events)    # result - events in form: [time, detector, energy]
            done=True
            print(f"INFO: Processed file {file_name}.")
        else:
            print(f"INFO: Waiting for RAM memory ({pu.virtual_memory()[2]}%).")
            time.sleep(5)   # wait for 5 seconds
    return energies

## MULTIPROCESSING - POOLING

# pooling (the method is understandably explained e.g. here: https://www.geeksforgeeks.org/synchronization-pooling-processes-python/)
cpu_c = mp.cpu_count()
if mp.cpu_count() > 4:
    cpu_c += -4

pool = mp.Pool(cpu_c)    # Pool object

energies = []

results = [pool.apply_async(processFile, args=(rf,)) for rf in raw_files]
for result, rf in zip(results, raw_files):
    try:
        energies.append(result.get(timeout=timeout))
    except mp.TimeoutError:
        print(f"WARNING: Unable to process file {rf} (timeout).")

energy_events = np.concatenate(energies)    # this returns all events with their energies in one numpy array
print('INFO: Multiprocessing ends.')


## EXPORT EVENTS TO CSV
if export_CSV:
    print(f'INFO: Export to CSV: "{CSV_name}"')
    data = {'time': energy_events[:,0],             # prepare CSV with headers
            'detector': energy_events[:,1],
            'energy': energy_events[:,2]
    }
    df = pd.DataFrame(data)                     # export to data folder using pandas
    df.to_csv(data_folder+"/"+CSV_name, sep='\t')
    print(f"INFO: CSV exported to {data_folder+"/"+CSV_name}")

# Clear RAM after multiprocessing if checked in settings
if os.name == 'posix' and POSIX_drop_cache_continuously:
    os.system("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
    print("INFO: RAM cache cleared.")

## MION CALIBRATION
if energy_calibration:
    mion_energy_eqiv = energyCalibration.calibrate(energy_events=energy_events)    # returned value is corresponds to 200 MeV
    print("INFO: Calibration ended.")
else:
    print('INFO: Calibration canceled.')


## END

# clear RAM cache if run on POSIX system
if os.name == 'posix' and POSIX_drop_cache:
    os.system("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
    print("INFO: RAM cache cleared.")

# end log
print(f"END: {datetime.datetime.now()}")