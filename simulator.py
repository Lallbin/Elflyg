import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
plt.close()

# Aircraft properties
drag_coef = 0.03
reference_area = 42     # (m^2)
weight = 10000          # (kg)
cruising_speed = 97    # (m/s)


# Other values
g = 9.82
altitude = 10000


def calculate_air_density(h):
    T0 = 288.15     # Sea level standard temperature (K)
    P0 = 101325     # Sea level standard pressure (Pa)
    L = -0.0065     # Temperature lapse rate (K/m)
    R = 287.058     # Specific gas constant for dry air (J/(kg*K))
    
    T = T0 + L * h # Temperature at given altitude (K)
    
    P = P0 * (T / T0) ** (-g / (R * L)) # Pressure at given altitude (Pa)
    
    rho = P / (R * T) # Air density at given altitude (kg/m^3)
    
    return rho


def calculate_drag_force(C_d0, rho, S, v): # Zero lift drag coefficient, air density, reference area, air speed
    D_p = (C_d0 * rho * S * v**2) / 2 # Parasitic drag
    D_i = 0 # Induced drag
    D_tot = D_p + D_i
    
    return D_tot

print(calculate_drag_force(drag_coef, calculate_air_density(altitude), reference_area, cruising_speed)*cruising_speed)

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