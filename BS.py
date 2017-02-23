'''This is personal program to return result of Black-Scholes formuala'''
import scipy.stats as st

norminv = st.distributions.norm.ppf; norm = st.distributions.norm.cdf
from numpy import sqrt,exp,log; import math; pai=math.pi
#define formula
def bsformula(callput, S0, K, r, T, sigma, q=0.):
    # define variables...
    d1=1/(sigma*sqrt(T))*(log(S0/K)+(r-q+0.5*(sigma**2))*T)
    d2=d1-sigma*sqrt(T)
    # define vega
    vega=S0*exp(-q*T)*sqrt(T)*1./sqrt(2*pai)*exp(-d1**2/2)

    # calculate options' value and delta in two types of options
    if callput==1:
        optionValue=S0*exp(-q*T)*norm(d1)-K*exp(-r*T)*norm(d2) # specification of call option
        delta=exp(-q*T)*norm(d1)
    if callput==-1:
        optionValue=K*exp(-r*T)*norm(-d2)-S0*exp(-q*T)*norm(-d1)
        delta=exp(-q*T)*(norm(d1)-1)
    return (optionValue,delta,vega)

if __name__=="__main__":
    a=bsformula(1, 50, 50, 0.1, 3.0-2.0, 0.1, q=0.)[0]
    print(a)

