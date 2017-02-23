from Gauss_Seidel_method import gauss
import numpy as np
import sys

def fdAmerican(callput, S0, K, r, T, sigma, q, M, N, S_max):

    ' input values'
    dt=T/N; ds=S_max/M; call_put='call'
    grid=np.zeros(shape=(M+1,N+1))
    i_values= np.arange(M+1)
    j_values= np.arange(N+1)
    boundary_conds=np.linspace(0,S_max,M+1)

    #setup coefficients
    alpha = 0.25 * dt * ((sigma ** 2) * (i_values ** 2) - (r - q) * i_values)
    beta = -dt * 0.5 * ((sigma ** 2) * (i_values ** 2) + r )
    gamma = 0.25 * dt * ((sigma ** 2) * (i_values ** 2) + (r - q) * i_values)
    M1 = -np.diag(alpha[2:M], -1) + np.diag(1 - beta[1:M]) - \
              np.diag(gamma[1:M - 1], 1)
    M2 = np.diag(alpha[2:M], -1) + np.diag(1 + beta[1:M]) + \
              np.diag(gamma[1:M - 1], 1)

    # setup boundary conditions and last column
    if callput==1: # call option
        past_values = np.maximum(boundary_conds[1:M]-K, 0)
        upperboundary_values = 0.0*j_values
        lowerboundary_values=np.maximum(S_max-K,0)*np.exp(-(r-q)*dt*(N-j_values))

    elif callput==-1: # put option
        past_values = np.maximum(K-boundary_conds[1:M], 0)
        upperboundary_values = K * np.exp(r * dt * (N - j_values))
        lowerboundary_values = np.maximum(K-S_max,0)*np.exp(-(r-q)*dt*(N-j_values))
    else:
        print('please input 1 for call options or -1 for put options')
        sys.exit()
    grid[:,-1][1:M]=past_values

    'travese grid'
    aux=np.zeros(M-1)
    for j in reversed(range(N)):
        aux[0]=alpha[1] * (upperboundary_values[j] + upperboundary_values[j+1])
        aux[-1] = gamma[M-1] * (lowerboundary_values[j] + lowerboundary_values[j+1])
        rhs=np.dot(M2,past_values)+aux

        # Gauss-Seidel method
        x=gauss(M1,rhs,100)

        if callput==1:
            new_values=np.maximum(x, boundary_conds[1:M]-K)
        elif callput==-1:
            new_values=np.maximum(x, K-boundary_conds[1:M])
        past_values=new_values
        grid[:,j][1:M]=new_values
    grid[0,:]=upperboundary_values
    grid[-1,:]=lowerboundary_values

    'interpolate'
    price=np.interp(S0,boundary_conds,grid[:,0])
    return price

if __name__ == "__main__":
    'test1 for Call options'
    test1= fdAmerican(1, 50, 50, 0.1, 0.5/12, 0.4, 0.01, 100, 100, 100)
    print(test1,'test1 for call options')

    test2 = fdAmerican(-1, 50, 50, 0.1, 0.5/12, 0.4, 0.01, 100, 100, 100)
    print(test2, 'test2 for put options')