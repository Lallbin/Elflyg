import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import flygplansklasser

plt.close()

# Aircraft properties
es_19 = flygplansklasser.Aircraft(8616, 37.7, 94, 92, 79, 4, 0, -3, 0.7)
es_30 = flygplansklasser.Aircraft(25000, 60, 97, 94, 80, 4, 0, -3, 0.7)

# Other values
g = 9.82

total_time = 60 * 60    # Seconds
time_step = 60 * 10         # Seconds per time step
time_points = np.arange(0, total_time, time_step)

total_distance = 400 * 1000

a_lift_coefficient = 0.11
b_lift_coefficient = 0.25
a_drag_coefficient = 0.0005
b_drag_coefficient = 0.0008
c_drag_coefficient = 0.0284





def cos(angle):
    return np.cos(np.radians(angle))
def tan(angle):
    return np.tan(np.radians(angle))

def sin(angle):
    return np.sin(np.radians(angle))

def tan(angle):
    return sin(angle) / cos(angle)

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
    C_l = 0.102 * a + 0.102
    
    return C_l

def calculate_lift_force(aircraft, a, alt, v):
    L = calculate_lift_coefficient(a) * 0.5 * calculate_air_density(alt) * aircraft.ref_area *  v ** 2
    
    return L

def calculate_angle_of_attack(aircraft, climb_angle_, altitude_, speed_):
    
    def func(a):
        L = calculate_lift_force(aircraft, a, altitude_, speed_)
        D = calculate_drag_force(aircraft, a, altitude_, speed_)
        
        return L * cos(climb_angle_) - D * sin(climb_angle_) + (L * sin(climb_angle_) + D * cos(climb_angle_)) * sin(a + climb_angle_) / cos(a + climb_angle_) - aircraft.weight * g
    
    return fsolve(func, 5)[0]

def calculate_thrust(aircraft, climb_angle_, altitude_, speed_):
    a = calculate_angle_of_attack(aircraft, climb_angle_, altitude_, speed_)
    L = calculate_lift_force(aircraft, a, altitude_, speed_)
    D = calculate_drag_force(aircraft, a, altitude_, speed_)
    
    F = (L * sin(climb_angle_) + D * cos(climb_angle_)) / cos(a + climb_angle_)
    
    if F < 0:
        raise ValueError("Calculated thrust is negative. Check input values.")
    
    return F

def energy_for_flight_phase(aircraft,altitude,climb_angle,speed):
    F = calculate_thrust(aircraft, climb_angle, altitude, speed)
    d = speed*time_step
    return F*d

def descent_distance_calc(aircraft, altitude):
    return altitude / tan(aircraft.descent_angle)

print(calculate_angle_of_attack(es_30, 0, 3000, es_30.cruise_speed))
print(calculate_thrust(es_30, 4, 3000, es_30.climb_speed))

print(calculate_lift_force(es_30, calculate_angle_of_attack(es_30, 4, 1500, 94), 1500, 94))
print(calculate_drag_force(es_30, calculate_angle_of_attack(es_30, 4, 1500, 94), 1500, 94))


def prel_main(aircraft):
    position = 0
    altitude = 0
    ground_speed = 0
    acceleration = 0
    angle_of_attack = 0
    climb_angle = 0
    energy_consumtion = 0

    positions = []
    altitudes = []
    ground_speeds = []
    accelerations = []
    angle_of_attacks = []
    climb_angles = []
    energy_consumtions = []
    
    t = 0
    flying = True
    while flying:
        t += time_step
        
        if altitude < 3000:
            climb_angle = aircraft.climb_angle
            ground_speed = aircraft.climb_speed * cos(climb_angle)
        elif total_distance - descent_distance_calc(aircraft, 3000) > position:
            climb_angle = aircraft.cruise_angle
            ground_speed = aircraft.cruise_speed * cos(climb_angle)
        else:
            climb_angle = aircraft.descent_angle
            ground_speed = aircraft.descent_speed * cos(climb_angle)
        
        
        position += ground_speed * time_step
        altitude += ground_speed * tan(climb_angle) * time_step
        energy_consumtion = energy_for_flight_phase(aircraft, altitude, climb_angle, ground_speed / cos(climb_angle)) / aircraft.propeller_efficiency
        
        positions.append(position)
        altitudes.append(altitude)
        ground_speeds.append(ground_speed)
        accelerations.append(acceleration)
        angle_of_attacks.append(angle_of_attack)
        climb_angles.append(climb_angle)
        energy_consumtions.append(energy_consumtion)
        
        if position >= total_distance:
            flying = False
            
    return sum(energy_consumtions), t

print()
print(prel_main(es_30)[0] / 3600000)
print((prel_main(es_30)[0] / 3600000) / (prel_main(es_30)[1] / 3600))

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