# script for determining energy of all events (Event) in given array and writing that to own CSV file

# importing libraries
import gc
import os
import pandas as pd

def eventsEnergy(events, noiseFile=""):
    print(f"INFO: Analyzing {len(events)} events.")

    # loading default noise file if not given
    if noiseFile == "":
        path = os.path.realpath(__file__)
        noiseFile = ""
        for s in path.split("/")[:-2]:      # obtaining script location
            noiseFile += s
            noiseFile += '/'
        noiseFile += "data/default_noise_levels.txt"

    # loading noise file
    noise_levels = pd.read_csv(noiseFile, header=None, sep='\t', usecols=[1])     # use only second column (not loading indieces)

    energies = []

    for event in events:
        energies.append(eventEnergy(event, noise_levels=noise_levels))

    # free RAM memory
    del events
    gc.collect()    # force it

    return energies

def eventEnergy(event, noise_levels):
    
    time = event.t
    detector = event.detector
    samples = event.samples

    # calculate energy

    energy = 1

    return [time, detector, energy]