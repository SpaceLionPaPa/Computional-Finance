import numpy as np
from numpy import mean, std
from numpy.random import randn, seed
from scipy.stats import norm
from BS import bsformula
#tes1
__mataclass__=type
class Dog:
    def bark(self, num):
        self.a=[]
        print(self.a)
        self.a = 'Woof! time is %f' % int(num)
        print(self.a)

    def newBark(self):
        print(self.a, "self.a in NewBark")

Dog().bark(0)
Dog().newBark()





'''S0 = 50; r = 0.025; T1 = 1; T2 = 2; sigma1 = 0.15; sigma2 = 0.15; X2 = S0
X1 = [bsformula(1, S0, X2, r, T2-T1, sigma2)[0], bsformula(-1, S0, X2, r, T2-T1, sigma2)[0]]
t1 = bsformula(1, Smin, X2, r, T2 - T1, sigma2)[0]
print("t1 is:", t1)'''

