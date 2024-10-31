# script for determining energy of all events (Event) in given array and writing that to own CSV file

# importing libraries
import gc

def eventEnergy(events):
    print(f"INFO: Analyzing {len(events)} events.")

    # free RAM memory
    del events
    gc.collect()    # force it
    # clear RAM cache if run on POSIX system
    if os.name == 'posix':
        os.system("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")