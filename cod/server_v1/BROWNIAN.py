from math import sqrt
from scipy.stats import norm
import numpy as np
import matplotlib
from pylab import plot, show, grid, xlabel, ylabel
from fracdiff import fdiff


""" Crea un array de ruido browniano """

def brownian(a, n, dt, delta, out=None):
    
    a = np.asarray(a)

    # Para cada elemento del array a, genera una muestra de n numeros en distribucion normal
    r = norm.rvs(size = a.shape + (n,), scale=delta*sqrt(dt))

    # Si no se proporciona un array de salida se genera uno
    if out is None:
        out = np.empty(r.shape)

    # Crea la tencendia browniana sumando la muestras aleatorias
    np.cumsum(r, axis=-1, out=out)

    # Anade la condicion incial.
    out += np.expand_dims(a, axis=-1)

    return out


if __name__ == "__main__":

    # The Wiener process parameter.
    delta = 4
    # Total time.
    T = 24*60
    # Number of steps.
    N = 500
    # Time step size
    dt = T/N
    # Number of realizations to generate.
    m = 2
    # Create an empty array to store the realizations.
    x = np.empty((m,N+1))
    # Initial values of x.
    x[:, 0] = 0
    
    brownian(x[:,0], N, dt, delta, out=x[:,1:])
    
    t = np.linspace(0.0, N*dt, N+1)
    fdiff(x[1], n=0.5)
    for k in range(m):
        plot(t, x[k])
        plot(t, x[1])
    xlabel('t', fontsize=16)
    ylabel('x', fontsize=16)
    grid(True)
    show()