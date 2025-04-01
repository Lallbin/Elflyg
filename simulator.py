import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import flygplansklasser

plt.close()

# Aircraft properties
es_19 = flygplansklasser.Aircraft(8616, 37.7, 94, 92, 79, 78, 4, 0, -3, 0.7, 1100)
es_30 = flygplansklasser.Aircraft(21000, 60, 97, 94, 80, 78, 4, 0, -3, 0.7, 1100)
lek_30 = flygplansklasser.Aircraft(25000, 70, 97, 94, 90, 57, 4, 0, -3, 0.8, 1100)

# Other values
g = 9.82

total_distance = 400 * 1000


# Gör så at cos/sin/tan funkar som vi vill att de ska göra
def cos(angle):
    return np.cos(np.radians(angle))

def sin(angle):
    return np.sin(np.radians(angle))

def tan(angle):
    return np.tan(np.radians(angle))

def calculate_air_density(h):
    T0 = 288.15     # Sea level standard temperature (K)
    P0 = 101325     # Sea level standard pressure (Pa)
    L = -0.0065     # Temperature lapse rate (K/m)
    R = 287.058     # Specific gas constant for dry air (J/(kg*K))
    
    T = T0 + L * h # Temperature at given altitude (K)
    
    P = P0 * (T / T0) ** (-g / (R * L)) # Pressure at given altitude (Pa)
    
    rho = P / (R * T) # Air density at given altitude (kg/m^3)
    
    return rho

def calculate_drag_coefficient(angle_of_attack_, flaps_):
    C_d = 0.025 + 0.035 * (calculate_lift_coefficient(angle_of_attack_, flaps_))**2
    
    return C_d

# Drag coefficient, air density, reference area, air speed
def calculate_drag_force(aircraft, aoa_, alt_, speed_, flaps_): 
    D = calculate_drag_coefficient(aoa_, flaps_) * 0.5 * calculate_air_density(alt_) * aircraft.ref_area *  speed_ ** 2
    
    return D

def calculate_lift_coefficient(angle_of_attack_, flaps_):

    C_l = 0.27 + 0.1 * angle_of_attack_ + flaps_ * 0.025
    
    return C_l


def calculate_lift_force(aircraft, aoa_, alt_, speed_, flaps_):
    L = calculate_lift_coefficient(aoa_, flaps_) * 0.5 * calculate_air_density(alt_) * aircraft.ref_area *  speed_ ** 2
    
    return L

#Beräknar vilken angle of attack som krävs för att hålla konstant fart vid en specifik tidpunkt. 
def calculate_angle_of_attack(aircraft, climb_angle_, altitude_, speed_, flaps_):
    
    def func(a):
        L = calculate_lift_force(aircraft, a, altitude_, speed_, flaps_)
        D = calculate_drag_force(aircraft, a, altitude_, speed_, flaps_)
        
        return L * cos(climb_angle_) - D * sin(climb_angle_) + (L * sin(climb_angle_) + D * cos(climb_angle_)) * sin(a + climb_angle_) / cos(a + climb_angle_) - aircraft.weight * g
    
    return fsolve(func, 5)[0]

#Beräknar thrust vid  en tidpunkt som krävs för att hålla konstant hastighet
def calculate_thrust(aircraft, climb_angle_, altitude_, speed_, flaps_):
    a = calculate_angle_of_attack(aircraft, climb_angle_, altitude_, speed_, flaps_)
    L = calculate_lift_force(aircraft, a, altitude_, speed_, flaps_)
    D = calculate_drag_force(aircraft, a, altitude_, speed_, flaps_)
    
    F = (L * sin(climb_angle_) + D * cos(climb_angle_)) / cos(a + climb_angle_)
    
    if F < 0:
        print(F, L, D, a, climb_angle_)
        raise ValueError("Calculated thrust is negative. Check input values.")
    
    return F

#Beräkna hur mycket energi flygplanet behöver för en viss tid. I loopen kör detta med ett lågt time step för att få alla steg i simulationen.
def energy_for_flight_phase(aircraft,altitude,climb_angle,speed,stage, max_thrust_, flaps_, time_step_):
    if stage < 1:
        F = max_thrust_
        d = speed*time_step_
    else: 
        F = calculate_thrust(aircraft, climb_angle, altitude, speed, flaps_)
        d = speed*time_step_
    return F*d

#Beräkna hur lång distans vi behöver för att komma ner till marken
def descent_distance_calc(aircraft, altitude): 
    return altitude / tan(aircraft.descent_angle)


#calculating takeoff accelleration assuming constant accelleration
def calculate_takeoff_acc(aircraft): # förslag att ge 300m till pre climb stadiet
    takeoff_time = (aircraft.runway)/(aircraft.climb_speed/2)
    return aircraft.climb_speed/takeoff_time

def calculate_takeoff_thrust(aircraft,a, altitude_, speed_):
    if speed_ >= 78:
        return aircraft.weight*calculate_takeoff_acc(aircraft)+(calculate_drag_coefficient(a)/calculate_lift_coefficient(a)*((speed_/aircraft.takeoff_speed)**2))*aircraft.weight*g
    
    else: 
        return aircraft.weight*calculate_takeoff_acc(aircraft) + calculate_drag_force(aircraft,a,altitude_,speed_)

def calculate_runway_acceleration(aircraft, F_max_, altitude_, speed_, flaps_):
    D = calculate_drag_force(aircraft, 0, altitude_, speed_, flaps_)
    acceleration_x_ = (F_max_ - D) / aircraft.weight
    
    return acceleration_x_

def calculate_takeoff_acceleration(aircraft, F_max_, angle_of_attack_takeoff_, climb_angle_, altitude_, speed_, flaps_):
    L = calculate_lift_force(aircraft, angle_of_attack_takeoff_, altitude_, speed_, flaps_)
    D = calculate_drag_force(aircraft, angle_of_attack_takeoff_, altitude_, speed_, flaps_)
    
    acceleration_x_ = (F_max_ * cos(angle_of_attack_takeoff_ + climb_angle_) - L * sin(climb_angle_) - D * cos(climb_angle_)) / aircraft.weight
    acceleration_y_ = (F_max_ * sin(angle_of_attack_takeoff_ + climb_angle_) + L * cos(climb_angle_) - D * sin(climb_angle_) - aircraft.weight * g) / aircraft.weight
    
    acceleration_ = (acceleration_x_**2 + acceleration_y_**2)**0.5
    
    return acceleration_x_, acceleration_y_, acceleration_
    
# Testvärden som skrevs för att testa värden, kommentera in ifall ni vill se ett värde

#print(calculate_angle_of_attack(es_30, 0, 3000, es_30.cruise_speed))
#print(calculate_thrust(es_30, 4, 3000, es_30.climb_speed))
#print(calculate_lift_force(es_30, calculate_angle_of_attack(es_30, 4, 1500, 94), 1500, 94))
#print(calculate_drag_force(es_30, calculate_angle_of_attack(es_30, 4, 1500, 94), 1500, 94))

def calculate_energy_density(aircraft,energy):
    battery_weight = aircraft.weight - 16000
    return energy/battery_weight

def prel_main(aircraft, max_thrust):
    stage = 0 # definierar vilken del av flygfasen vi är i, stage = 0 = takeoff, stage = 1 = climb, stage = 2 = cruise, stage = 3 = descent
    
    #Värden som beskriver flygplanets position och rörelse 
    t = 0
    time_step = 1
    
    position = 0
    altitude = 0
    
    speed_x = 0
    speed_y = 0
    speed = 0
    
    acceleration_x = 0
    acceleration_y = 0
    acceleration = 0
    
    angle_of_attack = 0
    climb_angle = 0
    
    energy_consumption = 0
    power_consumption = 0
    
    thrust = 0
    
    flaps = 0 # 0, 10, 20 or 30 (degrees)
    
    windspeed = 0

    #Listor med alla värden från hela flygturen
    t_list = []
    
    position_list = []
    altitude_list = []
    
    speed_x_list = []
    speed_y_list = []
    speed_list = []
    
    acceleration_x_list = []
    acceleration_y_list = []
    acceleration_list = []
    
    angle_of_attack_list = []
    climb_angle_list = []
    
    energy_consumption_list = []
    power_consumption_list = []
    
    thrust_list = []
    
    flaps_list = []
    
    
    #max_thrust = max_thrust / 2
    
    
    #Loopen vandrar i tid och kollar hur en flygfas ser ut genom att lägga varje punkt i en lista och 
    #sedan plotta den listan och summera energi för att få den totala energin.
    check = True
    flying = True
    descent_stall = False
    time_stall = 0
    while flying:
        t += time_step
        
        #if speed > 49 and check:
        #    max_thrust = max_thrust * 0.5
        #    check = False
        
        if stage == 0:
            #current_thrust = calculate_takeoff_thrust(aircraft,0, climb_angle, altitude, ground_speed)
            #ground_speed += current_thrust*time_step*cos(climb_angle)/aircraft.weight
            
            flaps = 20
            
            acceleration_x = calculate_runway_acceleration(aircraft, max_thrust, altitude, speed, flaps)
            acceleration = acceleration_x
            
            speed_x += acceleration_x * time_step
            speed += acceleration * time_step
            
            position += speed_x * time_step
            altitude += speed_y * time_step
            
            if speed > aircraft.takeoff_speed:
                stage = 0.5
                
        elif stage == 0.5:
            #climb_angle = aircraft.climb_angle
            #angle_of_attack = 10
            #current_thrust = calculate_takeoff_thrust(aircraft,angle_of_attack, climb_angle, altitude, ground_speed)
            #ground_speed += current_thrust*time_step*cos(climb_angle)/aircraft.weight
            #"pre climb" equations
            
            if speed > aircraft.takeoff_speed * 1.3:
                flaps = 10
            
            angle_of_attack = 8 - climb_angle
            
            acceleration_x, acceleration_y, acceleration = calculate_takeoff_acceleration(aircraft, max_thrust, angle_of_attack, climb_angle, altitude, speed, flaps)
            
            speed_x += acceleration_x * time_step
            speed_y += acceleration_y * time_step
            speed += acceleration * time_step
            
            climb_angle = np.degrees(np.arctan(speed_y / speed_x))
            
            position += speed_x * time_step
            altitude += speed_y * time_step
            
            if speed >= aircraft.climb_speed:
                stage = 1
                acceleration_x = 0
                acceleration_y = 0
                acceleration = 0
                flaps = 0
                
                
        
        elif stage == 1:      # Climb
            climb_angle = aircraft.climb_angle
            
            speed = aircraft.climb_speed
            speed_x = speed * cos(climb_angle)
            speed_y = speed * sin(climb_angle)
            
            position += (speed_x + windspeed) * time_step
            altitude += speed_y * time_step
            
            angle_of_attack = calculate_angle_of_attack(aircraft, climb_angle, altitude, speed, flaps)
            
            if altitude >= 3000: #Om vi är över vår cruising altitude går vi över till cruise
                stage = 2
        
        elif stage == 2:     # Cruise
            climb_angle = aircraft.cruise_angle
            
            speed = aircraft.cruise_speed
            speed_x = speed
            speed_y = 0
            
            position += (speed_x + windspeed) * time_step
            altitude += speed_y * time_step
            
            angle_of_attack = calculate_angle_of_attack(aircraft, climb_angle, altitude, speed, flaps)
            
            if total_distance + descent_distance_calc(aircraft, altitude) < position: #om vi har nått till det området när vi behöver stiga ner så går vi över till descent
                stage = 3
                print(calculate_lift_coefficient(angle_of_attack, flaps), calculate_drag_coefficient(angle_of_attack, flaps), calculate_lift_coefficient(angle_of_attack, flaps)/calculate_drag_coefficient(angle_of_attack, flaps), angle_of_attack)
        
        elif stage == 3:     # Descent
            if altitude < 1500 and time_stall <= 30*60:
                descent_stall = True
                    
            if descent_stall == True:
                climb_angle = aircraft.cruise_angle
                speed = aircraft.cruise_speed
                speed_x = speed
                speed_y = 0
                    
                angle_of_attack = calculate_angle_of_attack(aircraft, climb_angle, altitude, speed, flaps)
                time_stall += time_step
                if time_stall >= 30*60:
                    descent_stall = False
            elif descent_stall == False:
                climb_angle = aircraft.descent_angle
            
                speed = aircraft.descent_speed
                speed_x = speed * cos(climb_angle)
                speed_y = speed * sin(climb_angle)
            
                position += (speed_x + windspeed) * time_step
                altitude += speed_y * time_step
            
                angle_of_attack = calculate_angle_of_attack(aircraft, climb_angle, altitude, speed, flaps)       

        power_consumption = energy_for_flight_phase(aircraft, altitude, climb_angle, speed ,stage, max_thrust, flaps, time_step) / (aircraft.propeller_efficiency * time_step)
        energy_consumption += power_consumption * time_step / 3600000
        
        
        if stage < 1:
            thrust = max_thrust
        else:
            thrust = calculate_thrust(aircraft, climb_angle, altitude, speed, flaps)
        
        thrust_list.append(thrust)
        
        #lägg till alla värden i våra listor
        t_list.append(t)
        
        position_list.append(position)
        altitude_list.append(altitude)
        
        speed_x_list.append(speed_x)
        speed_y_list.append(speed_y)        
        speed_list.append(speed)
        
        acceleration_x_list.append(acceleration_x)
        acceleration_y_list.append(acceleration_y)
        acceleration_list.append(acceleration)
        
        angle_of_attack_list.append(angle_of_attack)
        climb_angle_list.append(climb_angle)
        
        energy_consumption_list.append(energy_consumption)
        power_consumption_list.append(power_consumption)
        
        flaps_list.append(flaps)
        
        if stage > 1 and altitude <= 1:
            flying = False
        
        #if position >= 1100:
        #    print(speed)
        #    print(acceleration_x)
        #    return altitude
    
    print(energy_consumption_list[-1]) #Printa totala energikonsumptionen och gör om till kWh
    print(t/3600) #tiden i timmar
    print(("Energy density", calculate_energy_density(aircraft,sum(energy_consumption_list)/(3600000 * time_step))))
    
    #Plotta flygturen med alla flygfaser
    """
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, flaps_list)
    plt.title("Flaps over time")
    plt.show()
    """
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, energy_consumption_list)
    plt.title("Energy consumption over time")
    plt.show()
    
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, power_consumption_list)
    plt.title("Power consumption over time")
    plt.show()
    
    """
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, altitude_list)
    plt.title("Altitude over time")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(t_list, thrust_list)
    plt.title("Thrust over time")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(t_list, angle_of_attack_list)
    plt.title("AOA over time")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(t_list, speed_x_list)
    plt.title("Ground speed over time")
    plt.show()
    
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, speed_list)
    plt.title("Speed over time")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(t_list, acceleration_list)
    plt.title("Acceleration over time")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(position_list, climb_angle_list)
    plt.title("Climb angle over distance")
    plt.show()
    
    plt.figure(figsize=(8, 5))
    plt.plot(position_list, altitude_list)
    plt.title("Altitude over distance")
    plt.show()

    """
    
    

def calculate_max_thrust(aircraft):
    def func(F):
        return prel_main(aircraft, F) - 15
    
    return fsolve(func, 63500)[0]
    

#print(calculate_max_thrust(lek_30))

prel_main(lek_30, 82000) # 52000
#prel_main(lek_30, 142800)
