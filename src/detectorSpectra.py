# script for creating histogram for each detector in events in pandas dataframe with columns [time, detector, energy]
# also filtering mions and fitting - returning x-coor for each detector (mion peak calibration)

# importin libraries
import pandas as pd
import numpy as np
import gc

def mion_filter_f(events, scrit=5e4, ncrit=3):
    # expected input: [[t1, t2, t3, .. tn], [e1, e2, e3, .. en]] and sorted by time (increasingly)

    self_energies = []
    for i in range(len(events[0])-ncrit):
        t1 = events[0][i]
        t2 = events[0][i+ncrit-1]
        if t2-t1 < scrit:
            if events[0][i+ncrit]-t1 < scrit:
                self_energies.append(events[1][i])
            else:
                for j in range(ncrit):
                    self_energies.append(events[1][i+j])
                i += ncrit-1
    return np.array(self_energies)


def mion_hist(df, mion_filter=True, n_detectors=84, bins=0, print_l1_info=False, print_warning=False, print_l2_info=False, debug_mode=False):
    # function returning filtered mion histogram for every detector

    # bins = 0 as automatic estimation of bins

    n_samples = df.shape[0]
    if bins == 0:
        bins = int(n_samples / n_detectors / 100)
        if bins < 10: bins = 10

    # result for return
    histograms = np.zeros((n_detectors, 2, bins+1))

    # sort dataframe and create an array of events for each detector
    df = df.sort_values(['detector', 'time'])
    if print_l2_info: print('INFO L2: CSV file sorted.')
    for i in range(n_detectors):
        detector_df = df[df['detector'] == float(i)]
        if mion_filter: 
            energies = mion_filter_f([list(detector_df['time']), list(detector_df['energy'])])
        else:
            energies = detector_df['energy']
        histograms[i,0,:-1], histograms[i,1] = np.histogram(energies, bins=bins)
        if print_l2_info: print(f'INFO L2: Creating histogram for detector {i}.')

    if print_l1_info: print('INFO L1: Detector histograms created.')

    return histograms