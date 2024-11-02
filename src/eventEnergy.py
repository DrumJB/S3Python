# script for determining energy of all events (Event) in given array and writing that to own CSV file

# importing libraries
import gc

def eventsEnergy(events):
    print(f"INFO: Analyzing {len(events)} events.")

    energies = []

    for event in events:
        energies.append(eventEnergy(event))

    # free RAM memory
    del events
    gc.collect()    # force it

    return energies

def eventEnergy(event):
    
    time = 1
    detector = 1
    energy = 1

    return [time, detector, energy]