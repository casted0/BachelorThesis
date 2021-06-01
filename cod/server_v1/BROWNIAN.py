from math import sqrt
from scipy.stats import norm
import numpy as np
import matplotlib
from pylab import plot, show, grid, xlabel, ylabel, legend
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
    
def fracdif_brownian(x):
    return fdiff(np.absolute(x), n=0.2)


if __name__ == "__main__":

    # The Wiener process parameter.
    delta = 2
    # Total time.
    T = 24*60
    # Number of steps.
    N = 24*60
    # Time step size
    dt = T/N
    # Create an empty array to store the realizations.
    x = np.empty((1,N+1))
    y = np.empty((1,N+1)) 
    # Initial values of x.
    x[:, 0] = 0
    y[:, 0] = 0
    
    brownian(x[:,0], N, dt, delta, out=x[:,1:])
    y[0] = x[0]
    print(x[0])
    t = np.linspace(0.0, N*dt, N+1)
    
    # En el caso de que el ruido generado sea negativo, no tiene sentido que no haya peticiones o sean negativas
    # asi que se usan los valores absolutos del ruido generado, que despues son suavizados para el script
    
    y = fracdif_brownian(x)
    
    print(y[0])
    
    plot(t, x[0], "-b", label="Original Array")
    plot(t, y[0], "-g", label="Fraccional diff Array")
    legend()
    xlabel('Time (minutes)', fontsize=16)
    ylabel('Requests (per Minute)', fontsize=16)
    grid(True)
    show()