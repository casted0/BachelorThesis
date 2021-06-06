import requests
import threading
import os
import BROWNIAN
import numpy as np
import time
from scipy.stats import norm
import matplotlib
from pylab import plot, show, grid, xlabel, ylabel, legend
from fracdiff import fdiff

url = "curl 192.168.1.46:8080"

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

plot(t, x[0], "-b", label="Original Array")
plot(t, y[0], "-g", label="Fraccional diff Array")
legend()
xlabel('Time (minutes)', fontsize=16)
ylabel('Requests (per Minute)', fontsize=16)
grid(True)
show()

f = open("Users.log", "w")

for i in range(y.size):


    print("Intervalo: ", i)
    print("Usuarios: ", int(y[0][i])*3)
    print("Peticiones por usuario: 5")
    print("Total de peticiones: ", int(y[0][i])*15)
    
    f.write("Intervalo: " + str(i))
    f.write("Usuarios: " + str(int(y[0][i])*3))
    f.write("Peticiones por usuario: 5")
    f.write("Total de peticiones: " + str(int(y[0][i])*15))
    f.write("\n\n")

    for j in range(int(y[0][i])*3):
        t = threading.Thread(target=curl)
        t.demon = True
        threadList.append(t)
        
    for j in range(int(y[0][i])*3):
        if not t.is_alive():
            threadList[j].start()
        
    for j in range(int(y[0][i])*3):
        threadList[j].join()
        
    threadList.clear()
    time.sleep(60)
        
            
f.close()
        
"""

En el array hay 60*24 items, la cantidad de minutos en un dia
por lo tanto esa es la cantidad de veces que se va a:

1. Crear n*2 hilos (Siendo n el numero del array en la iteracion correspondiente)
2. Cada hilo va a ejecutar 5 peticiones al servidor
    - Cada peticion hace una llamada simple que casi no consume tiempo, el resultado estara entre 0*2 y 50*3 a lo sumo *5 = unas 750 peticiones en un minuto

"""