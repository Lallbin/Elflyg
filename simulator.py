import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import flygplansklasser

plt.close()

# Aircraft properties
es_19 = flygplansklasser.Aircraft(8616, 37.7, 94, 92, 79, 4, 0, -3, 0.7)
es_30 = flygplansklasser.Aircraft(25000, 80, 97, 94, 97, 4, 0, -3, 0.7)

# Other values
g = 9.82

total_time = 60 * 60    # Seconds
time_step = 1         # Seconds per time step
time_points = np.arange(0, total_time, time_step)

total_distance = 400 * 1000

a_lift_coefficient = 0.11
b_lift_coefficient = 0.25
a_drag_coefficient = 0.0005
b_drag_coefficient = 0.0008
c_drag_coefficient = 0.0284




# Gör så at cos/sin/tan funkar som vi vill att de ska göra
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

# Drag coefficient, air density, reference area, air speed
def calculate_drag_force(aircraft, a, alt, v): 
    D = calculate_drag_coefficient(a) * 0.5 * calculate_air_density(alt) * aircraft.ref_area *  v ** 2
    
    return D

def calculate_lift_coefficient(a):
    C_l = 0.102 * a + 0.102
    
    return C_l


def calculate_lift_force(aircraft, a, alt, v):
    L = calculate_lift_coefficient(a) * 0.5 * calculate_air_density(alt) * aircraft.ref_area *  v ** 2
    
    return L

#Beräknar vilken angle of attack som krävs för att hålla konstant fart vid en specifik tidpunkt. 
def calculate_angle_of_attack(aircraft, climb_angle_, altitude_, speed_):
    
    def func(a):
        L = calculate_lift_force(aircraft, a, altitude_, speed_)
        D = calculate_drag_force(aircraft, a, altitude_, speed_)
        
        return L * cos(climb_angle_) - D * sin(climb_angle_) + (L * sin(climb_angle_) + D * cos(climb_angle_)) * sin(a + climb_angle_) / cos(a + climb_angle_) - aircraft.weight * g
    
    return fsolve(func, 5)[0]

#Beräknar thrust vid  en tidpunkt som krävs för att hålla konstant hastighet
def calculate_thrust(aircraft, climb_angle_, altitude_, speed_):
    a = calculate_angle_of_attack(aircraft, climb_angle_, altitude_, speed_)
    L = calculate_lift_force(aircraft, a, altitude_, speed_)
    D = calculate_drag_force(aircraft, a, altitude_, speed_)
    
    F = (L * sin(climb_angle_) + D * cos(climb_angle_)) / cos(a + climb_angle_)
    
    if F < 0:
        raise ValueError("Calculated thrust is negative. Check input values.")
    
    return F
#Beräkna hur mycket energi flygplanet behöver för en viss tid. I loopen kör detta med ett lågt time step för att få alla steg i simulationen.
def energy_for_flight_phase(aircraft,altitude,climb_angle,speed): 
    F = calculate_thrust(aircraft, climb_angle, altitude, speed)
    d = speed*time_step
    return F*d

#Beräkna hur lång distans vi behöver för att komma ner till marken
def descent_distance_calc(aircraft, altitude): 
    return altitude / tan(aircraft.descent_angle)

# Testvärden som skrevs för att testa värden, kommentera in ifall ni vill se ett värde
#print(calculate_angle_of_attack(es_30, 0, 3000, es_30.cruise_speed))
#print(calculate_thrust(es_30, 4, 3000, es_30.climb_speed))
#print(calculate_lift_force(es_30, calculate_angle_of_attack(es_30, 4, 1500, 94), 1500, 94))
#print(calculate_drag_force(es_30, calculate_angle_of_attack(es_30, 4, 1500, 94), 1500, 94))


def prel_main(aircraft):
    stage = 1 # definierar vilken del av flygfasen vi är i stage = 1 = climb, stage = 2 = cruise, stage = 3 = descent
    
    t = 0
    position = 0
    altitude = 0
    ground_speed = 0
    acceleration = 0
    angle_of_attack = 0
    climb_angle = 0
    energy_consumtion = 0

    times = []
    positions = []
    altitudes = []
    ground_speeds = []
    accelerations = []
    angle_of_attacks = []
    climb_angles = []
    energy_consumtions = []
    
    #Loopen vandrar i tid och kollar hur en flygfas ser ut genom att lägga varje punkt i en lista och 
    #sedan plotta den listan och summera energi för att få den totala energin.
    flying = True
    while flying:
        t += time_step
        
        if stage == 1:      # Climb
            climb_angle = aircraft.climb_angle
            ground_speed = aircraft.climb_speed * cos(climb_angle)
            
            if altitude >= 3000:
                stage = 2
        
        elif stage == 2:     # Cruise
            climb_angle = aircraft.cruise_angle
            ground_speed = aircraft.cruise_speed * cos(climb_angle)
            
            if total_distance + descent_distance_calc(aircraft, 3000) < position:
                stage = 3
        
        elif stage == 3:     # Descent
            climb_angle = aircraft.descent_angle
            ground_speed = aircraft.descent_speed * cos(climb_angle)
        
        #uppdatera position, angle of attack och den energin som krävs för att ta sig dit.
        position += ground_speed * time_step
        altitude += ground_speed * tan(climb_angle) * time_step
        angle_of_attack = calculate_angle_of_attack(aircraft, climb_angle, altitude, ground_speed / cos(climb_angle))
        energy_consumtion = energy_for_flight_phase(aircraft, altitude, climb_angle, ground_speed / cos(climb_angle)) / aircraft.propeller_efficiency
        
        #lägg till alla värden i våra listor
        times.append(t)
        positions.append(position)
        altitudes.append(altitude)
        ground_speeds.append(ground_speed)
        accelerations.append(acceleration)
        angle_of_attacks.append(angle_of_attack)
        climb_angles.append(climb_angle)
        energy_consumtions.append(energy_consumtion)
        
        if position >= total_distance:
            flying = False
    
    print(sum(energy_consumtions) / 3600000)
    print(t/3600)
    
    #Plotta flygturen med alla flygfaser
    plt.figure(figsize=(8, 5))
    plt.plot(positions, altitudes)
    plt.title("Altitude over distance")
    plt.xlabel("Distance (m)")
    plt.ylabel("Altitude (m)")
    plt.show()
    
    #Plotta an figur på hur våra angle of attacks ser ut. 
    plt.figure(figsize=(8, 5))
    plt.plot(positions, angle_of_attacks)
    plt.title("AOA over distance")
    plt.xlabel("Distance (m)")
    plt.ylabel("AOA (degrees)")
    plt.show()
    
prel_main(es_30)





