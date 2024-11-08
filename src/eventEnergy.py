# script for determining energy of all events (Event) in given array and writing that to own CSV file

# importing libraries
import gc
import os
import pandas as pd
import scipy.integrate as si
import numpy as np

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
        print(f"WARNING: No noise file given, using default file: {noiseFile}.")

    # loading noise file
    noise_levels = pd.read_csv(noiseFile, names=['noise'], sep='\t', usecols=[1])     # use only second column (not loading indices)
    print(f"INFO: Noise levels loaded from {noiseFile}.")

    energies = []
    print_n_out = 4
    print_out = [False for i in range(print_n_out)]      # print status every 10%
    for i in range(len(events)):
        energies.append(eventEnergy(events[i], noise_levels=noise_levels))
        progress = int(i/len(events)*print_n_out)
        if not print_out[progress]:
            print_out[progress] = True
            print(f"INFO: Energy event analysis progress (individual process): {int(progress*100/print_n_out)}%.")

    # free RAM memory
    del events
    gc.collect()    # force it

    return energies

def eventEnergy(event, noise_levels):
    
    # loading variables
    time = event.t
    detector = event.detector
    samples = event.samples
    noise_level = noise_levels['noise'][detector-1]      # detector 1 = noise_levels[0]

    # subtract noise level from samples
    data = []
    for sample in samples:
        data.append(sample - noise_level)
    
    # integrate
    interval = 1e-8     # time step is 10 ns
    x = np.linspace(0, len(samples)*interval, len(samples))
    #for i in range(len(data)-1):
    #    rectangle = data[i]*interval                    # simple geometry
    #    triangle = (data[i+1]-data[i])*interval/2
    #    energy += rectangle + triangle
    energy = si.trapezoid(samples, x=x)
    energy = energy * 1/32768       # normalizing to 'correct' zero in -1 V using half of the number of bins (65568) 

    return [time, int(detector), energy]