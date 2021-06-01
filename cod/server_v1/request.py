import requests
import threading
import os
import BROWNIAN
import numpy as np
import time

url = "curl 127.0.0.1:8080"

def curl():
    for i in range(5):
        os.system(url)

threadList = []

    
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

BROWNIAN.brownian(x[:,0], N, dt, delta, out=x[:,1:])
y[0] = x[0]
t = np.linspace(0.0, N*dt, N+1)

# En el caso de que el ruido generado sea negativo, no tiene sentido que no haya peticiones o sean negativas
# asi que se usan los valores absolutos del ruido generado, que despues son suavizados para el script

y = BROWNIAN.fracdif_brownian(x)

for i in range(y.size):


    print("Minuto: ", i)
    print("Peticiones: ", int(y[0][i]))

    for j in range(int(y[0][i])*2):
        t = threading.Thread(target=curl)
        t.demon = True
        threadList.append(t)
        
    for j in range(int(y[0][i])*2):
        if not t.is_alive():
            threadList[j].start()
        
    for j in range(int(y[0][i])*2):
        threadList[j].join()
        
    threadList.clear()
        
        
        
        
"""

En el array hay 60*24 items, la cantidad de minutos en un dia
por lo tanto esa es la cantidad de veces que se va a:

1. Crear n*2 hilos (Siendo n el numero del array en la iteracion correspondiente)
2. Cada hilo va a ejecutar 5 peticiones al servidor
    - Cada peticion hace una llamada simple que casi no consume tiempo, el resultado estara entre 0*2 y 50*2 a lo sumo *5 = unas 500 peticiones en un minuto

"""