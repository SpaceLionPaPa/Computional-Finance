# write a function to combine your BSMonteCarlo and MCStockPrices func-tions
from MCStockPrices import MCStockPrices
import numpy as np
from numpy import exp,sqrt,maximum,mean,array,std
from numpy.random import rand
import sys

'define funciton'
def MCOptionPrices( S0, K, T, rateCurve, sigma, t, checkpoints, samples, integrator):
    # Use linear interpolation to find rate
    tenors=[1.,3.,6.,12.,24.,36.,60.]
    r=np.interp(T,tenors,rateCurve)

    # raise exception
    try:
        lastSamplePoint=samples[:,checkpoints[-1]-1] # samples (when specified) must be a list with at least as many elements as the last entry in checkpoints.
    except:
        print('The length of sample is short than the length of checking point')
        sys.exit()

    # for different integrator
    if integrator == 'standard':
        S_ts = MCStockPrices(S0, sigma, rateCurve, t, samples, 'standard')
    if integrator == 'euler':
        S_ts = MCStockPrices(S0, sigma, rateCurve, t, samples, 'euler')
    if integrator == 'milstein':
        S_ts = MCStockPrices(S0, sigma, rateCurve, t, samples, 'milstein')
    S_T= S_ts[-1,:] #underlying asset's price in maturity time

    # specify data structure
    TV=np.zeros((1,2)); Means = np.zeros((len(checkpoints),2))
    StdDevs=np.zeros((len(checkpoints),2)); StdErrs=np.zeros((len(checkpoints),2))
    # i is the running check point
    num = 0
    for i in checkpoints:
        calls_running = exp(-r * (T / 12.)) * maximum(0.0, S_T[0:i-1]-K)  # call option values of different paths
        puts_running = exp(-r * (T / 12.)) * maximum(0.0, K-S_T[0:i-1])  # put option values of different paths
        Means[num] = array([mean(calls_running), mean(puts_running)])  # The running mean at each checkpoint
        StdDevs[num] = array([std(calls_running), std(puts_running)])  # The running standard deviation at each checkpoint
        StdErrs[num] = array(StdDevs[num] / sqrt(i))  # The running standard error at each checkpoint
        num += 1
    TV = Means[-1]
    return {'TV':TV, 'Means':Means, 'StdDevs':StdDevs, 'StdErrs':StdErrs}

'test fuction'
if __name__ =="__main__":
    from BS import bsformula
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    # test MCOptionPrices function with fixed M and N
    # 09/20/16 yield curve
    rateCurve = array([0.17, 0.30, 0.49, 0.61, 0.79, 0.93, 1.20]) * 0.01
    checkpoints = [1000, 2000, 5000, 10000, 20000, 50000]
    S0 = 50.; K = 55.; sigma = 0.1; T = 10.  # Monthly
    M = checkpoints[-1]; N = 100
    t = array([T / N] * N)  # Monthly
    samples1 = rand(N, M)
    # results in different methods Standard
    for u in ['standard','euler','milstein']: # test in different integrator methods
        test=MCOptionPrices(S0, K, T, rateCurve, sigma, t, checkpoints, samples1, u)
        TV = test['TV']
        print('Using %s method, Call option TV is %.5f' % (u, TV[0]))
        print('Means are',test['Means'])

    # test error properties
    tenors=[1.,3.,6.,12.,24.,36.,60.]
    r=np.interp(T,tenors,rateCurve)

    m=range(100,2010,100); n=range(1,101,1) # create dynamic M and N
    print('Varied N is %s'%n,'Varied M is %s'%m)
    'Vary N'
    error_n=np.zeros((len(n),3))
    checkpoints2 = [10,m[-1]]
    num1_1=0
    for k in n:
        samples2 = rand(k, m[-1])
        t2 = array([T / k] * k)  # Monthly
        num2_1 = 0
        for u in ['standard', 'euler', 'milstein']: # calculate error in different integrator methods
            test= MCOptionPrices(S0, K, T, rateCurve, sigma, t2, checkpoints2, samples2, u)
            TV = test['TV']
            error_n[num1_1,num2_1] = abs(TV[0] - bsformula(1, S0, K, r, T / 12., sigma)[0])
            num2_1+=1
        num1_1+=1

    'Vary M'
    error_m = np.zeros((len(m), 3))
    t2 = array([T / n[-1]] * n[-1])  # Monthly
    num1_2=0
    for l in m:
        samples2 = rand(n[-1], l)
        checkpoints2 = [10,l]
        num2_2 = 0
        for u in ['standard', 'euler', 'milstein']: # calculate error in different integrator methods
            test = MCOptionPrices(S0, K, T, rateCurve, sigma, t2, checkpoints2, samples2, u)
            TV = test['TV']
            error_m[num1_2, num2_2] = abs(TV[0] - bsformula(1, S0, K, r, T / 12., sigma)[0])
            num2_2 += 1
        num1_2 += 1

    'plot error'
    nm=[n,m]; error=[error_n,error_m] #unify data structure
    q=1
    for w in ['N','M']:
        plt.figure(q,figsize=(7,4))
        num=0
        for u in ['standard', 'euler', 'milstein']: # plot error in different integrator methods
            plt.plot(nm[q-1], error[q-1][:,num], lw=1.5, label='%s method' %u)
            plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
            num += 1
        plt.axis('tight')
        plt.xlabel('%s' % w)
        plt.ylabel('error value')
        plt.title('Vary %s' % w)
        q+=1
    plt.show()
