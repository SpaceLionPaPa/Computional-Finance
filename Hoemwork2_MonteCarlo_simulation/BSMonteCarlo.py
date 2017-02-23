# Write a function to price european-exercise options in one step
import numpy as np
from numpy import exp,sqrt,maximum,mean,array,std
from numpy.random import randn
import sys
'define BSMonteCarlo function'
def BSMonteCarlo( S0, K, T, sigma, checkpoints, rateCurve, samples=None):
    if samples is None:
        samples=randn(1,checkpoints[-1]) #create samples for all checkpoints, and time step is 1 for problem1

    # if samples are given
    # raise exception
    try:
        lastSamplePoint=samples[0,checkpoints[-1]-1] # samples (when specified) must be a list with at least as many elements as the last entry in checkpoints.
    except:
        print('The length of sample is short than the length of checking point')
        sys.exit()

    # specify data structure
    TV=np.zeros((1,2)); Means = np.zeros((len(checkpoints),2))
    StdDevs=np.zeros((len(checkpoints),2)); StdErrs=np.zeros((len(checkpoints),2))

    # Use linear interpolation to find rate
    tenors=[1.,3.,6.,12.,24.,36.,60.]
    r=np.interp(T,tenors,rateCurve)
    print('r is %.4f' %r)

    num = 0
    # i is the running check point
    for i in checkpoints:
        sample_running = samples[0,0:i-1]
        S_T_running= S0*exp((r-0.5*sigma**2)*(T/12.) + sigma*sqrt(T/12.)*sample_running)
        calls_running= exp(-r * (T/12.)) * maximum(0.0, S_T_running - K) # call option values of different paths
        puts_running= exp(-r * (T/12.)) * maximum(0.0, K - S_T_running) # put option values of different paths
        Means[num]= array([mean(calls_running),mean(puts_running)]) # The running mean at each checkpoint
        StdDevs[num]=array([std(calls_running),std(puts_running)]) # The running standard deviation at each checkpoint
        StdErrs[num]=array(StdDevs[num]/sqrt(i)) # The running standard error at each checkpoint
        num+=1
    TV=Means[-1]
    return {'TV':TV,'Means':Means,'StdDevs':StdDevs,'StdErrs':StdErrs}  # The end of function

"Test BSMonteCarlo function and plot"
if __name__ =="__main__":
    from numpy import array, transpose
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    # input value
    # 09/20/16 yield curve
    M=1000000; N=1
    rateCurve = array([0.17, 0.30, 0.49, 0.61, 0.79, 0.93, 1.20]) * 0.01
    checkpoints = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]
    S0 = 50.; K = 55.; sigma = 0.1; T = 10.  # Monthly

    'when the shape of sample is not small than the last entry in checkpoints'
    test1 = BSMonteCarlo(S0, K, T, sigma, checkpoints, rateCurve, randn(N,M))
    TV=test1['TV']
    print('Call option TV is %.3f' %TV[0],'Put option TV is%.3f' %TV[1])

    'Plot test'
    # plot Means, StdDevs, and StdErrs in check points
    k=1
    for w in ['Means','StdDevs','StdErrs']:
        plt.figure(k)
        plt.plot(checkpoints, transpose(test1[w])[0], 'bo-', label='%s_Call' %w)
        plt.axis('tight')
        plt.xlabel('checkpoints')
        plt.ylabel('value')
        plt.title('%s in different ckecking point' %w )
        plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
        k+=1
    plt.show()

    'when the shape of sample is small than the last entry in checkpoints'
    print('when M=1000')
    test2 = BSMonteCarlo(S0, K, T, sigma, checkpoints, rateCurve, randn(1,10000))

