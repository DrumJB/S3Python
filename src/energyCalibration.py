# script for calibrating detector using mion peak

# importing libraries
import numpy as np
import scipy.integrate as si
import scipy.optimize as so
import matplotlib.pyplot as pp

def calibrate(energy_events, simultaneity=1e-5, mion_crit=5):

    print("INFO: Calibration started.")
    print("INFO: Looking for simultaneous events.")
    
    # energy_events are in shape [[time1, detector1, energy1], [time2, detector2, ...] ...]

    energies = []

    print('INFO: Sorting events.')
    energy_events = energy_events[np.argsort(energy_events[:, 0])]  # sort events by time (first in array)

    for i in range(len(energy_events)-mion_crit):
        print(f"INFO: Event scan progress: {round(i/len(energy_events)*100, 2)}%", end='\r')
        t1 = energy_events[i][0]
        t2 = energy_events[i+mion_crit-1][0]
        if t2 - t1 < simultaneity:
            if energy_events[i+mion_crit][0]-t1 < simultaneity:     # longer row of simultaneous events than mion_crit
                energies.append(energy_events[i][2])
            else:
                for j in range(mion_crit):                          # append with the rest and add it to i
                    energies.append(energy_events[i+j][2])
                i += mion_crit
    
    print(f"INFO: Event scan progress: 100% .. DONE")
    
    print(f"INFO: {len(energies)} simultaneous events found.")
    
    print("INFO: Landau fit started.")

    ## LANDAU FIT
    landau_inf = 100
    def landau(x, mu, c):
            x_int = np.linspace(1e-3, landau_inf, 5000)
            y_int = [np.e**(-t) * np.cos(t*(x-mu)/c + 2*t/np.pi*np.log(t/c)) for t in x_int]
            return 1/(np.pi*c) * si.simpson(y_int, x=x_int)

    def landau_arr(x, mu, c):
        result = [] 
        for given_x in x:
            result.append(landau(given_x, mu, c))
        return result
    
    # energies to histogram
    y, x = np.histogram(energies, bins=int(len(energies)/6))

    print("INFO: Histogram created.")

    # normalize for landau fit
    xmin = x[0]
    xmax = x[-1]
    xdiff = xmax-xmin
    norm_x = []
    for nx in x:
        norm_x.append((nx-(xmin))*15/(xdiff)-5)
    
    #ymin = 0  - assumption
    ymax = np.max(y)
    norm_y = []
    for ny in y:
        norm_y.append(ny*0.2/ymax)

    print("INFO: Starting fit using scipy.optimize.curve_fit")

    guess = (0, np.pi/2)


    plot_result = True
    if plot_result:
        pp.plot(norm_x[:-1], norm_y)
        pp.show()

    # fitting landau curve
    param, param_cov = so.curve_fit(landau_arr, norm_x[:-1], norm_y, p0=guess)

    print(f"INFO: Data fitted using Landau distribution mu = {param[0]}, c = {param[1]}")

    # determining maximum of landau curve
    landau_discrete_n = 100
    x2 = np.linspace(norm_x[0], norm_x[-1], landau_discrete_n)
    landau_discrete = [landau(i, param[0], param[1]) for i in x2]
    max_x = 0
    maximum = 0         # want to find x-coord of maximum (in y)
    for i in range(landau_discrete_n): 
        if landau_discrete[i]>maximum: 
            maximum=landau_discrete[i]
            max_x = i
    
    mu_energy = (x2[max_x]+5)*xdiff/15 + xmin    # denormalize as x

    print(f"INFO: Mion energy obtained: 200MeV ~ {mu_energy}.")
    print(f"INFO: Plotting resulted fit...")
    plot_result = True
    if plot_result:
        pp.plot(norm_x[:-1], norm_y)
        pp.plot(x2, landau_discrete)
        pp.show()

    return mu_energy
    
