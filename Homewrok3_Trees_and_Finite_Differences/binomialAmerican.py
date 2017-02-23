import numpy as np
import math

def binomialAmerican(S0, Ks, r, T, sigma, q, callputs, M):
    # setup parameters
    dt=T/float(M)
    u=math.exp(sigma*math.sqrt(dt));  d=1./u
    print(u,'u')
    qu=(math.exp((r-q)*dt)-d)/(u-d); qd=1-qu
    df=math.exp(-(r-q)*dt)
    num_nod=M+1
    print(qu,'qu')
    # initialize stock pirce tree
    STs=[np.array([S0])]
    # Simulate the possible stock price path
    for i in range(M):
        prev_brances=STs[-1]
        st=np.concatenate((prev_brances*u,[prev_brances[-1]*d]))
        STs.append(st) # add nodes at each time step

    #for different elements in array
    l=len(Ks)
    payoffs= [0]*l; not_ex_payoffs=[0]*l; ex_payoffs=[0]*l; price= [0]*l
    for w in range(l):
        #initialize payoffs tree
        # payoff at in T time
        if callputs[w] == 1: # call option
            payoffs[w]= np.maximum(0.,STs[M]-Ks[w])
        else:  # put option
            payoffs[w]= np.maximum(Ks[w]-STs[M],0.)

        #traverse_tree
        for i in reversed(range(M)):
            # The payoff from not exercising the option
            not_ex_payoffs[w]=(payoffs[w][:-1]*qu+payoffs[w][1:]*qd)*df
            # early_exercise
            if callputs == 1:
                ex_payoffs[w]=(STs[i]-Ks[w])
            else:
                ex_payoffs[w]=(Ks[w]-STs[i])
            payoffs[w]= np.maximum(not_ex_payoffs[w],ex_payoffs[w])
        price[w]=payoffs[w][0]
        print(price[w], '%sth price of the array' % (w + 1))
    return price

if __name__=='__main__':
    test=binomialAmerican(50,[45,50,55,45,50,55], 0.1, 0.5/12, 0.4, 0.01, [1,1,1,-1,-1,-1], 100)
    print(test,'test')

