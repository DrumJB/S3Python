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
import random
import gc

import readFile
import eventEnergy
import detectorSpectra
import fitting

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
temp_folder = './temp'
export_histograms = True

# levels of printing:
print_warning = True
print_l1_info = True
print_l2_info = False

# calibrate
energy_calibration = settings['main']['energy_calibration']

# processFile timeout
timeout = settings["run_config"]["processFile_timeout"]
timeout_fit = 120

# maximum RAM usage
max_RAM_usage = settings["run_config"]["max_RAM_usage"]
POSIX_drop_cache = settings["run_config"]["POSIX_drop_cache"]
POSIX_drop_cache_continuously = settings["run_config"]["POSIX_drop_cache_continuously"]

# clear RAM cache if run on POSIX system
if os.name == 'posix' and POSIX_drop_cache:
    os.system("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
    if print_l1_info: print("INFO L1: RAM cache cleared.")


# clearing temp folder with user dialog
delete_temp = input(f'The temporary folder ({temp_folder}) will be cleared now. OK? y/[n]   ->  ')
if delete_temp == 'y':
    os.system(f'rm -r {temp_folder}')
    os.system(f'mkdir {temp_folder}')
else:
    print('ERROR: Could not clear temporary folder. This will often lead to merged results with another run.')
df = pd.DataFrame(columns=['time', 'detector', 'energy'])                     # export to data folder using pandas
df.to_csv(temp_folder+"/"+CSV_name, sep='\t', mode='a', index=False)

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

## EXPORT EVENTS TO CSV
def export_CSV_func(energy_events, where):
    data = {'time': energy_events[:,0],             # prepare CSV with headers
            'detector': energy_events[:,1],
            'energy': energy_events[:,2]
    }
    df = pd.DataFrame(data, columns=None)                     # export to data folder using pandas
    df.to_csv(where+"/"+CSV_name, sep='\t', mode='a', index=False, header=False)


## PROCESSING FUNCTION

# function for processing one file, called in Pool
def processFile(file_name):
    done = False
    events, energies = [], []
    while not done:     # try to run the job if not done
        if pu.virtual_memory()[2]/100 < max_RAM_usage:
            events = readFile.readFile(file_name, print_warning=print_warning, print_l2_info=print_l2_info)
            energies = eventEnergy.eventsEnergy(events, print_l2_info=print_l2_info, print_warning=print_warning)    # result - events in form: [time, detector, energy]
            done=True
            if print_l1_info: print(f"INFO L1: Processed file {file_name}.")
        else:
            if print_l2_info: print(f'INFO L2: Waiting for free RAM memory space (currently {pu.virtual_memory()[2]}%)')
            time.sleep(5)

    export_CSV_func(np.array(energies), temp_folder)
    if print_l2_info: print('INFO L2: Temporary CSV mereged with file in temp folder.')
    del energies

    return False

## MULTIPROCESSING - POOLING

# pooling (the method is understandably explained e.g. here: https://www.geeksforgeeks.org/synchronization-pooling-processes-python/)
cpu_c = mp.cpu_count()
if mp.cpu_count() > 4:
    cpu_c += -4

pool = mp.Pool(cpu_c)    # Pool object

results = [pool.apply_async(processFile, args=(rf,)) for rf in raw_files]
for result, rf in zip(results, raw_files):
    try:
        res = result.get(timeout=timeout)
        del result
        gc.collect()
    except mp.TimeoutError:
        if print_warning: print(f"WARNING: Unable to process file {rf} (timeout).")
        del result
        gc.collect()

if print_l1_info: print('INFO L1: Multiprocessing ends.')

# delete all residues
del pool
gc.collect()

# Clear RAM after multiprocessing if checked in settings
if os.name == 'posix' and POSIX_drop_cache_continuously:
    os.system("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
    if print_l1_info: print("INFO L1: RAM cache cleared.")


## MION CALIBRATION

# saving histograms to CSV


# histogram distribution fitting multiprocessing function
def fit_hist(histb):
    peak_x = fitting.fit_hist(histb, debug_mode=debug_mode)
    if debug_mode: print('DEBUG: Fitting MP process completed')
    return peak_x

# mutliprocessing inicializer and runner
def mp_fitting(histograms):
    calibrations = []
    pool = mp.Pool(cpu_c)
    processes = [pool.apply_async(fit_hist, args=(histb,)) for histb in histograms]
    for p in processes:
        try:
            calibrations.append(p.get(timeout=timeout_fit))
            del p
            gc.collect()
        except mp.TimeoutError:
            if print_warning: print(f"WARNING: Unable to fit histogram (timeout).")
            del p
            gc.collect()
    return calibrations

if energy_calibration:
    df = pd.read_csv(temp_folder+"/"+CSV_name, sep='\t')
    if debug_mode: print('DEBUG: CSV loaded.')
    histograms = detectorSpectra.mion_hist(df, 
                                           debug_mode=debug_mode, print_l1_info=print_l1_info, 
                                           print_warning=print_warning, print_l2_info=print_l2_info)
    if debug_mode: print('DEBUG: Histograms created.')
    del df
    gc.collect()
    calibrations = mp_fitting(histograms)
    print(calibrations)


    if print_l1_info: print("INFO L1: Calibration ended.")
else:
    if print_l1_info: print('INFO L1: Calibration canceled.')


## END

# clear RAM cache if run on POSIX system
if os.name == 'posix' and POSIX_drop_cache:
    os.system("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
    if print_l1_info: print("INFO L1: RAM cache cleared.")

# end log
print(f"END: {datetime.datetime.now()}")
