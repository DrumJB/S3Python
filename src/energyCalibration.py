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

    times = []
    energies = []

    ############ DEBUG!!!!!!!!!!!!
    energy_events = energy_events[:10000]

    # find simultaneous events
    for i in range(len(energy_events)):
        event = energy_events[i]
        print(f"INFO: Event scan progress: {round(i/len(energy_events)*100, 2)}%", end='\r')
        # don't check if already included in result
        included = False
        for t in times:
            if abs(event[0]-t) < simultaneity:
                included = True
        # check with all other events for simultaneity
        if not included:
            sim_events = []
            for j in range(i, len(energy_events)):
                e = energy_events[j]
                if abs(e[0]-event[0])<simultaneity:
                    sim_events.append(e)
            
            # mion criterion - at least 5 simultaneous events
            if len(sim_events) >= mion_crit:
                times.append(event[0])
                for se in sim_events:
                    energies.append(se[2])
    
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

    guess = (0.077, 0.010)

    # fitting landau curve
    param, param_cov = so.curve_fit(landau_arr, x[:-1], y, guess)

    print(f"INFO: Data fitted using Landau distribution mu = {param[0]}, c = {param[1]}")

    # determining maximum of landau curve
    landau_discrete_n = 100
    x2 = np.linspace(x[0], x[-1], landau_discrete_n)
    landau_discrete = [landau(i, param[0], param[1]) for i in x2]
    max_x = 0
    maximum = 0         # want to find x-coord of maximum (in y)
    for i in range(landau_discrete_n): 
        if landau_discrete[i]>maximum: 
            maximum=landau_discrete[i]
            max_x = i
    mu_energy = x2[max_x]

    print(f"INFO: Mion energy obtained: 200MeV ~ {mu_energy}.")

    plot_result = True
    if plot_result:
        pp.plot(x[:-1], y)
        pp.plot(x2, landau_discrete)
        pp.show()

    return mu_energy
    
