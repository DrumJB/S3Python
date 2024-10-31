# script for determining energy of all events (Event) in given array and writing that to own CSV file

# importing libraries
import gc
import os

def eventEnergy(events):
    print(f"INFO: Analyzing {len(events)} events.")

    # free RAM memory
    del events
    gc.collect()    # force it