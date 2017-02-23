# Write a function to price european-exercise options using MonteCarlo Methods in multiple steps
import numpy as np
from numpy import exp,sqrt,array,shape,sum
from numpy.random import rand
import scipy.stats as st
norminv = st.distributions.norm.ppf

'define funciton'
def MCStockPrices(S0, sigma, rateCurve, t, samples, integrator):
    # Use linear interpolation to find rate
    T=sum(t)# Monthly
    tenors = [1., 3., 6., 12., 24., 36., 60.]
    r = np.interp(T, tenors, rateCurve)

    # transform uniform samples to standard normal distribution
    z=norminv(samples)
    l1, l2 = shape(z)
    S_t=np.zeros((l1+1,l2)); S_t[0,:]=S0
    i=1# start from second time point
    for dt in t:
        # for different integrator
        if integrator =='standard':
            S_t[i,:] = S_t[i-1,:]* exp((r- 0.5* sigma** 2)* (dt/12.)+ sigma* sqrt(dt/12.)*z[i-1,:])
        if integrator =='euler':
            S_t[i,:] = S_t[i-1,:]* (1.+ r*dt/12.+ sigma*sqrt(dt/12.)*z[i-1,:])
        if integrator == 'milstein':
            S_t[i,:]= S_t[i-1,:]* (1.+(r)*dt/12.+ sigma*sqrt(dt/12.)*z[i-1,:]+ 0.5*sigma*sigma*(z[i-1,:]**2*(dt/12.)-dt/12.))
        i += 1
    SP_ts=S_t[1:,:] #let simulated stock prices having the same dimensions as samples.
    return SP_ts

'test MCStockPrices function'
if __name__ =="__main__":
    #input value
    # 09/20/16 yield curve
    rateCurve= array([0.17, 0.30, 0.49, 0.61, 0.79, 0.93, 1.20]) * 0.01
    M=10000; N=365; S0=50.; sigma=0.1; t=array([10./N]*N) #Monthly
    samples=rand(N,M)
    test1= MCStockPrices(S0, sigma, rateCurve, t, samples, 'standard')
    print(test1,shape(test1))
    test2= MCStockPrices(S0, sigma, rateCurve, t, samples,'euler')
    print(test2,shape(test2))
    test3= MCStockPrices(S0, sigma, rateCurve, t, samples, 'milstein')
    print(test2,shape(test2))