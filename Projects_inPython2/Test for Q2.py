"""Test for Q2"""
import numpy as np
from Q2_CompoundOption_Var_Vol import Comp_Opt_Var_Vol
from numpy import exp, sqrt, maximum,mean, array, std, floor
from BS import bsformula
import time

#The start time
# Set primary values
S0, r, T1, T2 = [50.0, 0.025, 1.0, 2.0]; X2 = S0
# Different client's view
views = {'Mrs Smith': ([r + 0.03, 0.15], [r + 0.005, 0.3]), 'Mr Johnson': ([r - 0.03, 0.2], [r - 0.01, 0.18]),
         'Ms Williams': ([r - 0.03, 0.18], [r + 0.03, 0.12]), 'Mr Jones': ([r + 0.02, 0.35], [r + 0.02, 0.1]),
         'Miss Brown': ([r + 0.03, 0.15], [r - 0.05, 0.15])}
names = ('Mrs Smith', 'Mr Johnson', 'Ms Williams', 'Mr Jones', 'Miss Brown')

# in different views
'Question c1-Antithetic Sampling methods. ComOpt4 and ComOpt5 is the prices of compound options'
ComOpt4 = [0] * len(names); option = ('Call', 'Put')
ComOpt5 = [0] * len(names)
j = 0
for v in names:
    mu1, sigma1, mu2, sigma2 = views[v][0][0], views[v][0][1], views[v][1][0], views[v][1][1]
    # At the money
    X1 = [bsformula(1, S0, X2, r, T2 - T1, sigma2)[0], bsformula(-1, S0, X2, r, T2 - T1, sigma2)[0]]

    print()
    print("Antithetic Sampling")
    # For different underlying options
    ComOpt4[j] = [0] * 2; i = 0
    for underlying in option:
        # Antithetic Sampling
        start_c1 = time.clock()
        ComOpt4[j][i] = [0] * 4
        ComOpt4[j][i] = Comp_Opt_Var_Vol(S0, X1, X2, r, T1, T2, mu1, mu2, sigma1,
                        sigma2).antiSampling(underlying, int(10000), 777)
        # Get enough size of number to satisfy The Central Limit Theorem
        N = int(floor(std(ComOpt4[j][i][3]) ** 2.0 * 1.96 ** 2.0 * 1002001 /
                      (mean(ComOpt4[j][i][3]) ** 2.0)))
        print("Using Antithetic Sampling, simulaiton number is", N)
        ComOpt4[j][i] = Comp_Opt_Var_Vol(S0, X1, X2, r, T1, T2, mu1, mu2, sigma1,
                        sigma2).antiSampling(underlying, N, 777)
        print("For %s, the price of Call on %s and Put on %s are %f and %f"
              % (v, underlying, underlying, ComOpt4[j][i][0], ComOpt4[j][i][1]))
        print("And the Confidence of Interval is", ComOpt4[j][i][2])
        i += 1
    end_c1 = time.clock()
    print("The running time is : %.03f seconds" % (end_c1 - start_c1))
    j += 1

'Question c2-Control Variates methods. ComOpt5 is the prices of compound options'
ComOpt5 = [0] * len(names); option = ('Call', 'Put')
j = 0
for v in names:
    mu1, sigma1, mu2, sigma2 = views[v][0][0], views[v][0][1], views[v][1][0], views[v][1][1]
    # At the money
    X1 = [bsformula(1, S0, X2, r, T2 - T1, sigma2)[0], bsformula(-1, S0, X2, r, T2 - T1, sigma2)[0]]

    print()
    print("Control Variates")
    # For different underlying options
    ComOpt5[j] = [0] * 2; i = 0
    for underlying in option:
        # Control Variates
        start_c2 = time.clock()
        ComOpt5[j][i] = [0] * 4
        ComOpt5[j][i] = Comp_Opt_Var_Vol(S0, X1, X2, r, T1, T2, mu1, mu2, sigma1,
                        sigma2).controlVariates(underlying, int(10000), int(10000), 777)
        # Get enough size of number to satisfy The Central Limit Theorem
        N = int(floor(std(ComOpt5[j][i][3]) ** 2.0 * 1.96 ** 2.0 * 1002001 /
                      (mean(ComOpt5[j][i][3]) ** 2.0)))
        print("Using Control Variates, simulaiton number is", N)
        ComOpt5[j][i] = Comp_Opt_Var_Vol(S0, X1, X2, r, T1, T2, mu1, mu2, sigma1,
                        sigma2).controlVariates(underlying, N, int(10000), 777)
        print("For %s, the price of Call on %s and Put on %s are %f and %f"
              % (v, underlying, underlying, ComOpt5[j][i][0], ComOpt5[j][i][1]))
        print("And the Confidence of Interval is", ComOpt5[j][i][2])
        i += 1
    end_c2 = time.clock()
    print("The running time is : %.03f seconds" % (end_c2 - start_c2))
    j += 1
# End
