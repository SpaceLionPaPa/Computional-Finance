import numpy as np


def gauss(A, b, w, tol=1e-10):
    L_hat = np.tril(A)  # Returns the lower triangular matrix of A
    U = A - L_hat  # Decompose A = L_hat + U
    L_inv = np.linalg.inv(L_hat)
    x = np.zeros_like(b)

    for i in range(w):
        Ux = np.dot(U, x)
        x_new = np.dot(L_inv, b - Ux)

        if np.allclose(x, x_new, tol):
            break

        x = x_new

    return x

if __name__ == '__main__':
    A = np.array([[10., -1., 2., 0.],
                  [-1., 11., -1., 3.],
                  [2., -1., 10., -1.],
                  [0.0, 3., -1., 8.]])
    b = np.array([6., 25., -11., 15.])
    w = 100
    x = gauss(A, b, w)
    print "x =", x