'create newton method fuction and create bsimpvol function and test bsimpvol function'
from Bisect import bisect; from BS import bsformula
'define newton method'
def newton_Method(target,y,dy,x,tols=[0.001,0.01],maxiter=1000):
    n=1
    while n<=maxiter:
        x1= x-(y(x)-target)/dy(x)
        if abs(x1-x)<tols[0] or abs(y(x1)-target)<tols[1]:# close to target
            return x1, n
        else:
            x=x1;n+=1
    # raise exception
    try:
        raise
    except:
        return 'the number of iteration is %d' % n, "There is no solution after all iteration"

'define bsimpvol formula'
def bsimpvol(callput,S0,K,r,T,price,q=0.0,priceTollerance=0.01,method='bisect',reportCalls=False):
#judge which method to use
    'return NaN'
    # no input value
    input_Value = [callput, S0, K, r, T]
    if all(input_Value) is False:
        return 'NaN'
    # price is less than intrinsic value
    if callput==1:
        if price<max(0,S0-K):
            return 'NaN'
    if callput==-1:
        if price<max(0,K-S0):
            return 'NaN'

    # call bsformula
    # create f function and df for methods
    def optionValue(x):
        return bsformula(callput, S0, K, r, T, x, q)[0]
    def optVega(x):
        return bsformula(callput, S0, K, r, T, x, q)[2]

    # use bisection method
    if method == 'bisect':
        (volatility,callsTimes) = bisect(price,optionValue,0.001, [-0.001, 15], [0.001,priceTollerance],1000)
        #if reportCalls is true
        if reportCalls==True:
            return (volatility[callsTimes-1],callsTimes)
        else:
            return volatility[callsTimes-1]
    # use newton method
    elif method == 'newton':
        (volatility,callsTimes) = newton_Method(price,optionValue,optVega,0.8,[0.001,priceTollerance],1000)
        #if reportCalls is true
        if reportCalls==True:
            return (volatility,callsTimes)
        else:
            return volatility
    else:
        print("please input 'bisect' or 'newton' in method")

'Test BSImplVol only in this file'
if __name__=='__main__':
    # ATM #At the money options
    print "ATM"
    call_ATM_Newton= bsimpvol(1, 50.0, 50.0, 0.1, 2.0, 10, 0.0, 0.01, 'newton', True)
    call_ATM_Bisect= bsimpvol(1, 50.0, 50.0, 0.1, 2.0, 10, 0.0, 0.01, 'bisect', True)
    put_ATM_Newton= bsimpvol(-1, 50.0, 50.0, 0.1, 2.0, 1, 0.0, 0.01, 'newton', True)
    put_ATM_Bisect= bsimpvol(-1, 50.0, 50.0, 0.1, 2.0, 1, 0.0, 0.01, 'bisect', True)
    print 'newton method', call_ATM_Newton
    print 'bisect method', call_ATM_Bisect
    print 'newton method',put_ATM_Newton
    print 'bisect method',put_ATM_Bisect

    # ITM #In the money options
    print "ITM"
    call_ITM_Newton=bsimpvol(1, 50.0, 45.0, 0.1, 2.0, 15.0, 0.0, 0.01, 'newton', True)
    call_ITM_Bisect=bsimpvol(1, 50.0, 45.0, 0.1, 2.0, 15.0, 0.0, 0.01, 'bisect', True)
    put_ITM_Newton=bsimpvol(-1, 50.0, 55.0, 0.1, 2.0, 6.0, 0.0, 0.01, 'newton', True)
    put_ITM_Bisect=bsimpvol(-1, 50.0, 55.0, 0.1, 2.0, 6.0, 0.0, 0.01, 'bisect', True)
    print 'newton method',call_ITM_Newton
    print 'bisect method',call_ITM_Bisect
    print 'newton method',put_ITM_Newton
    print 'bisect method',put_ITM_Bisect

    # OTM #Out of money options
    print "OTM"
    call_OTM_Newton=bsimpvol(1, 50.0, 55.0, 0.1, 2.0, 6.0, 0.0, 0.01, 'newton', True)
    call_OTM_Bisect=bsimpvol(1, 50.0, 55.0, 0.1, 2.0, 6.0, 0.0, 0.01, 'bisect', True)
    put_OTM_Newton=bsimpvol(-1, 50.0, 45.0, 0.1, 2.0, 6.0, 0.0, 0.01, 'newton', True)
    put_OTM_Bisect=bsimpvol(-1, 50.0, 45.0, 0.1, 2.0, 6.0, 0.0, 0.01, 'bisect', True)
    print 'newton method',call_OTM_Newton
    print 'bisect method',call_OTM_Bisect
    print 'newton method',put_OTM_Newton
    print 'bisect method',put_OTM_Bisect
