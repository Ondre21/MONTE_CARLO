# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:42:59 2020

@author: mitta
"""

import numpy as np
from numpy import prod
from scipy.spatial import distance

"""
The EP probability density function reads:
f(x; b, a, m) = 1/[2ab**(1/b) * L * (1 + 1/b )] * e**(-1/b | x-m/a|**b


where a > 0, b > 0 and L(·) is the Gamma function.
The EP is a generalization of a Gaussian random variable, and it is fully characterized by
three parameters: a location parameter m, a scale parameter a and a shape parameter b. The
location parameter controls for the mean of the distribution, whereas the scale parameter is
proportional to the absolute deviation5. The parameter b determines the fatness of the tails:
the larger b, the thinner the tails. In particular, as visualized in Figure 1, if b = 2, the EP
distribution reduces to a Gaussian, whereas if b = 1, one recovers a Laplace (with unit standard
deviation if a = 1/
p2).
The EP distribution allows one to precisely measure how far the empirical distribution is
from the normal and Laplace benchmarks. Note also that the EP density is characterized by
exponentially-shaped tails, and thus it has finite moments of any order. This is important, as
in many financial applications one typically deals with heavy-tails distributions whose higher
moments (and sometimes even the mean) do not converge (Embrechts et al., 1997). Macroeconomic growth-rate time-series distributions, conversely, almost always possess finite moments.
Therefore, we do not expect, at least in principle, RBC and NK macroeconomic model to badly
behave with such smooth shock distributions


mean = .45 # potential quarterly real gdp growth from FRED
a = (1/(2**.5)) # static scale
#numpy.random.laplace(loc=0.0, scale=1.0, size=None)
sample = np.random.laplace(m, a, 5000)/100 #m/100 put in proper units

import seaborn as sb
from matplotlib import pyplot as plt
\
sb.distplot(sample,kde = False)
plt.show()
"""


given_mean =.45
quarters_forecasting = 8
divisor = 100
forecasts_to_create = 100000
quarters_to_perc = 4
forecast_prob = .90 #higher is worse

class monte_carlo_forecaster:

    def __init__(self, name):
        self.name = name

    def randomization(self, given_mean, divisor, quarters_forecasting, forecasts_to_create):
        all_arrays = []
        all_arrays1 = []

        for x in range(forecasts_to_create):
            single_output = np.random.laplace(given_mean, (1/(2**.5)), quarters_forecasting)/divisor #m/100 put in proper units)
            single_output1 = [x+1 for x in single_output]
            all_arrays.append(single_output)
            all_arrays1.append(single_output1)
            
#        print(firstyear_perc)
#        print("")
#        print(frstyrfullreturn_list)
        return(all_arrays, all_arrays1)

            
    def cumulative_return(self, all_arrays, all_arrays1, forecast_prob, quarters_to_perc):
        firstyear_list = []
        fullreturn_list = []
        frstyrfullreturn_list = []

        for single_output1 in all_arrays1:            
            firstyearreturn = (prod(single_output1[:quarters_to_perc]))-1 # gets product of first perc
    #       print(str("firstyearreturn"))
    #       print(str(firstyearreturn))
    
            fullreturn = (prod(single_output1[:quarters_forecasting]))-1
    #       print(str("fullreturn"))
    #       print(str(fullreturn))
            frstyrfullreturn = [firstyearreturn, fullreturn]
    #       print(frstyrfullreturn)
    
            firstyear_list.append(firstyearreturn)
            fullreturn_list.append(fullreturn)
            frstyrfullreturn_list.append(frstyrfullreturn) ############    
        return(firstyear_list, frstyrfullreturn_list)
    
    def percentile_getter(self, perc, firstyear_list):
        firstyear_perc = np.percentile(firstyear_list,perc)
        return(firstyear_perc)

   
    def return_to_baseline(self, given_mean, divisor, quarters_forecasting):
        baseline_return = (1+given_mean/divisor)**quarters_forecasting-1  # switch this out with the baseline forecast
#        print(baseline_return)
#        print("")
        return(baseline_return)
        
    def target(self, firstyear_perc, baseline_return):
        target1 = [firstyear_perc, baseline_return]
        print("Target:" + str(target1))
        return(target1)
        
    def closest(self, target1, frstyrfullreturn_list, all_arrays):
        closest1 = min(frstyrfullreturn_list, key=lambda c : distance.euclidean(c, target1))
        shocked_iloc = frstyrfullreturn_list.index(closest1)
        closest_array = all_arrays[shocked_iloc] 
        print("Closest" + str(closest1))
        print('closest_array:' + str(closest_array))
        print(closest_array[:quarters_to_perc])

        return(closest1, closest_array)
        
        

def main():
    GDP = monte_carlo_forecaster("GDP")
    all_arrays, all_arrays1 = GDP.randomization(given_mean, 100, quarters_forecasting, forecasts_to_create)
    firstyear_list, frstyrfullreturn_list = GDP.cumulative_return(all_arrays, all_arrays1, forecast_prob, quarters_to_perc)
    firstyear_perc = GDP.percentile_getter(forecast_prob, firstyear_list)
    baseline_return = GDP.return_to_baseline(given_mean, divisor, quarters_forecasting)
    target1 = GDP.target(firstyear_perc, baseline_return)
    closest_array = GDP.closest(target1, frstyrfullreturn_list, all_arrays)
    # closest_array is the 

if __name__ == "__main__":
  main()
