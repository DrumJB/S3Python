# script for fitting L, LG, or LG convoluted to given histogram and returning the peak x-coor

import numpy as np
import scipy.integrate as si
import scipy.optimize as so
import time as t

def fit_hist(histb, timeout = 60, distribution='Langauss', debug_mode=False):
    
    bins = histb[1]
    hist = histb[0]
    progress = []
    landau_inf = 100

    print(hist, bins)

    def landau(x, mu, c):
        x_int = np.linspace(1e-3, landau_inf, 5000)
        y_int = [np.e**(-t) * np.cos(t*(x-mu)/c + 2*t/np.pi*np.log(t/c)) for t in x_int]
        return 1/(np.pi*c) * si.simpson(y_int, x=x_int)

    def landau_mse(param):
        mu = param[0]
        c = param[1]
        scale = param[2]
        result = []
        x = bins[:-1]
        for given_x in x:
            result.append(landau(given_x, mu, c)*scale)
        fit = np.array(result)
        mse = (np.square(fit-hist)).mean()
        progress.append(mse)
        return mse
    
    def landau(x, mu, c):
        x_int = np.linspace(1e-3, landau_inf, 5000)
        y_int = [np.e**(-t) * np.cos(t*(x-mu)/c + 2*t/np.pi*np.log(t/c)) for t in x_int]
        return 1/(np.pi*c) * si.simpson(y_int, x=x_int)

    def gauss(x, mu, sigma):
        const = 1/(np.sqrt(2*np.pi*sigma**2))
        exponential = np.exp((-((x-mu)**2)) / (2*sigma**2))
        return const*exponential

    def langau_mse(param):
        mu_landau = param[0]
        c = param[1]
        scale = param[2]
        mu_gauss = param[3]
        sigma = param[4]
        result = []
        x = bins[:-1]
        for given_x in x:
            result.append(landau(given_x, mu_landau, c)*scale * gauss(given_x, mu_gauss, sigma))
        fit = np.array(result)
        mse = (np.square(fit-hist)).mean()
        progress.append(mse)
        return mse
    
    def langau_conv_mse(param):
        mu_landau = param[0]
        c = param[1]
        scale = param[2]
        mu_gauss = param[3]
        sigma = param[4]
        langau_result = []
        x = bins[:-1]
        for given_x in x:
            langau_result.append(landau(given_x, mu_landau, c)*scale * gauss(given_x, mu_gauss, sigma))
        fit = np.convolve(np.array(langau_result), np.array(langau_result), 'same')     # convolution
        mse = (np.square(fit-hist)).mean()
        progress.append(mse)
        return mse

    class Stopper:
        def __init__(self, max_sec=30):
            self.max_sec = max_sec
            self.start = t.time()
        def stopIteration(self, xk):
            if (t.time() - self.start) > self.max_sec:
                raise StopIteration
    
    func = [[], []]
    if distribution == 'Landau':
        func = [landau_mse, [1000, 80, 40000]]
    elif distribution == 'Langauss':
        func = [langau_mse, []]
    elif distribution == 'CLangauss':
        func = [langau_conv_mse, []]
    else:
        print(f'ERROR fatal: Invalid distribution selected {distribution}.')
        return False

    stopper = Stopper(max_sec=timeout)
    res_landau = so.minimize(func[0], func[1], method='Nelder-Mead', callback=stopper.stopIteration)
    print(f'Final MSE: {landau_mse(res_landau.x)}')
    
