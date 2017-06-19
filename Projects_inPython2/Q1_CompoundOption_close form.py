'''This is first program for term project of Derivatives modeling. And this program is aim to price
compound options in closed form'''
'Run successfully in 3.0 version'
import numpy as np
from BS import bsformula
from scipy.stats import mvn, norm
from scipy.optimize import fsolve
# define function to price compound opitions' prices
def Compound_Option_Pricing_Closed_Form(S0, X1, X2, r, T1, T2, sigma):
    # Use fslove and Black Scholes formula to sovle I
    f1 = lambda I: bsformula(1, I, X2, r, T2 - T1, sigma)[0] - X1[0]
    f2 = lambda I: bsformula(-1, I, X2, r, T2 - T1, sigma)[0] - X1[1]
    I = [fsolve(f1, S0), fsolve(f2, S0)]; I = np.array(I)

    y1 = (np.log((S0) / I) + (r + sigma ** 2 / 2) * T1) / (sigma * np.sqrt(T1))
    y2 = y1 - sigma * np.sqrt(T1)
    z1 = (np.log((S0) / X2) + (r + sigma ** 2 / 2) * T2) / (sigma * np.sqrt(T2))
    z2 = z1 - sigma * np.sqrt(T2)
    rho = np.sqrt(T1 / T2)

    # Compound option pricing
    low = np.array([-np.inf, -np.inf]); M = mvn.mvndst  # mvn.mvndst(low,upp,[0,0],rho)[1]  if INFIN(I) = 0, integration range is (-infinity, UPPER(I)
    CC = S0 * M(low, np.array([z1, y1[0]]), [0, 0], rho)[1] - \
         X2 * np.exp(-r * T2) * M(low, np.array([z2, y2[0]]), [0, 0], rho)[1] - \
         X1[0] * np.exp(-r * T1) * norm.cdf(y2[0])
    PC = X2 * np.exp(-r * T2) * M(low, np.array([z2, -y2[0]]), [0, 0], -rho)[1] - \
         S0 * M(low, np.array([z1, -y1[0]]), [0, 0], -rho)[1] + \
         X1[0] * np.exp(-r * T1) * norm.cdf(-y2[0])

    CP = X2 * np.exp(-r * T2) * M(low, np.array([-z2, -y2[1]]), [0, 0], rho)[1] - \
         S0 * M(low, np.array([-z1, -y1[1]]), [0, 0], rho)[1] - \
         X1[1] * np.exp(-r * T1) * norm.cdf(-y2[1])
    PP = S0 * M(low, np.array([-z1, y1[1]]), [0, 0], -rho)[1] - \
         X2 * np.exp(-r * T2) * M(low, np.array([-z2, y2[1]]), [0, 0], -rho)[1] + \
         X1[1] * np.exp(-r * T1) * norm.cdf(y2[1])
    return (CC, PC, CP, PP)

# Test above function in this py file
if __name__ == "__main__":
    # input values
    S0, r, T1, T2, sigma, X2 = [50, 0.025, 1.0, 2.0, 0.15, 50.0]
    # At the money compound options
    X1 = [bsformula(1, S0, X2, r, T2 - T1, sigma)[0], bsformula(-1, S0, X2, r, T2 - T1, sigma)[0]]
    price = Compound_Option_Pricing_Closed_Form(S0, X1, X2, r, T1, T2, sigma); cn = 0
    for w in ['Call on Call', 'Put on Call', 'Call on Put', 'Put on Put']:
        print('%s compound opiton price is %f ' % (w, price[cn]))
        cn += 1
