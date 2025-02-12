import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import flygplansklasser
plt.close()

# Aircraft properties
es_19 = flygplansklasser.Aircraft(8616, 37.7, 94, 4, 0, -3)
es_30 = flygplansklasser.Aircraft(21000, 60, 97, 4, 0, -3)

# Other values
g = 9.82

total_time = 60 * 60    # Seconds
time_step = 0.1         # Seconds per time step
time_points = np.arange(0, total_time, time_step)


def calculate_air_density(h):
    T0 = 288.15     # Sea level standard temperature (K)
    P0 = 101325     # Sea level standard pressure (Pa)
    L = -0.0065     # Temperature lapse rate (K/m)
    R = 287.058     # Specific gas constant for dry air (J/(kg*K))
    
    T = T0 + L * h # Temperature at given altitude (K)
    
    P = P0 * (T / T0) ** (-g / (R * L)) # Pressure at given altitude (Pa)
    
    rho = P / (R * T) # Air density at given altitude (kg/m^3)
    
    return rho

def calculate_drag_coefficient(a):
    C_d = 0.0005 * a ** 2 - 0.0008 * a + 0.0284
    
    return C_d

def calculate_drag_force(aircraft, a, alt, v): # Drag coefficient, air density, reference area, air speed
    D = calculate_drag_coefficient(a) * 0.5 * calculate_air_density(alt) * aircraft.ref_area *  v ** 2
    
    return D

def calculate_lift_coefficient(a):
    C_l = 0.11 * a + 0.25
    
    return C_l

def calculate_lift_force(aircraft, a, alt, v):
    L = calculate_lift_coefficient(a) * 0.5 * calculate_air_density(alt) * aircraft.ref_area *  v ** 2
    
    return L

def calculate_gamma(aircraft, altitude,speed, weight):
    for gamma in range(1,20,0.01):
        L = calculate_lift_force(aircraft,gamma,altitude,speed)
        if L == weight*g:
            return gamma
    if gamma <=20:
        print("ERROR MESSAGE: gamma is greater than 20 degrees. Something is wierd")
    
print(calculate_lift_force(es_30, 5.86, 4000, es_30.cruise_speed))
print(es_30.weight * g)

"""
air_density_list = []
altitude_list = np.linspace(0, 11000, 111)
for altitude in altitude_list:
    air_density_list.append(calculate_air_density(altitude))



plt.figure(figsize=(8, 5))
plt.plot(air_density_list, altitude_list)
plt.title("Air density vs altitude")
plt.xlabel("Air density (kg/m^3)")
plt.ylabel("Altitude (m)")
plt.show()
"""