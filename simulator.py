import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import flygplansklasser
import propeller

plt.close()

# Aircraft properties
es_19 = flygplansklasser.Aircraft(8616, 37.7, 94, 92, 79, 78, 4, 0, -3, 2000000, 1100)
es_30 = flygplansklasser.Aircraft(21000, 60, 97, 94, 80, 78, 4, 0, -3, 2000000, 1100)
lek_30 = flygplansklasser.Aircraft(21400, 77, 97, 94, 90, 68, 4, 0, -3, 2300000, 1375)

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

def calculate_lift_coefficient(angle_of_attack_, flaps_):
    #C_l = 0.27 + 0.1 * angle_of_attack_ + flaps_ * 0.025
    C_l = 0.20 + 0.105 * angle_of_attack_ + flaps_ * 0.025
    
    return C_l

def calculate_drag_coefficient(angle_of_attack_, flaps_):
    #C_d = 0.025 + 0.039 * (calculate_lift_coefficient(angle_of_attack_, flaps_))**2 
    C_d = 0.025 + 0.039 * (calculate_lift_coefficient(angle_of_attack_, flaps_))**2 
    
    # UPPDATERA SÅ ATT L/D blir 19,8 vid cruise!!!
    
    return C_d

def calculate_lift_force(aircraft, aoa_, alt_, speed_, flaps_):
    L = calculate_lift_coefficient(aoa_, flaps_) * 0.5 * calculate_air_density(alt_) * aircraft.ref_area *  speed_ ** 2
    
    return L

def calculate_drag_force(aircraft, aoa_, alt_, speed_, flaps_): 
    D = calculate_drag_coefficient(aoa_, flaps_) * 0.5 * calculate_air_density(alt_) * aircraft.ref_area *  speed_ ** 2
    
    return D

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
def energy_for_flight_phase(aircraft,altitude,climb_angle,speed,stage, thrust_, flaps_, time_step_):
    if stage < 1:
        F = thrust_
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
    battery_weight = aircraft.weight - 13400
    return energy/battery_weight


def prel_main(aircraft, time_step=1.0, max_power=lek_30.max_motor_power, takeoff_calculation=False):
    stage = 0 # definierar vilken del av flygfasen vi är i, stage = 0 = takeoff, stage = 1 = climb, stage = 2 = cruise, stage = 3 = descent
    cruise_alt = 3500
    runway = 1385
    #Värden som beskriver flygplanets position och rörelse 
    t = 0
    
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
    
    aircraft_efficiency = 1

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
    
    aircraft_efficiency_list = []
    
    
    #Loopen vandrar i tid och kollar hur en flygfas ser ut genom att lägga varje punkt i en lista och 
    #sedan plotta den listan och summera energi för att få den totala energin.
    flying = True
    descent_stall = False
    one_motor = False
    first = True
    time_stall = 0
    while flying:
        t += time_step
        
        if speed > aircraft.takeoff_speed and not one_motor and takeoff_calculation:
            #max_power *= 0.5
            one_motor = True
        
        if stage == 0:
            flaps = 20
            
            thrust, aircraft_efficiency = propeller.prop_thrust_from_motor_power(max_power, calculate_air_density(altitude), speed)
            #print(thrust, 1)
            
            if not one_motor:
                thrust *= 2
            
            acceleration_x = calculate_runway_acceleration(aircraft, thrust, altitude, speed, flaps)
            acceleration = acceleration_x
            
            speed_x += acceleration_x * time_step
            speed += acceleration * time_step
            
            position += speed_x * time_step
            altitude += speed_y * time_step
            
            if first:
                first = False
            
            if speed > aircraft.takeoff_speed:
                stage = 0.5
                first = True
                
        elif stage == 0.5:
            #climb_angle = aircraft.climb_angle
            #angle_of_attack = 10
            #current_thrust = calculate_takeoff_thrust(aircraft,angle_of_attack, climb_angle, altitude, ground_speed)
            #ground_speed += current_thrust*time_step*cos(climb_angle)/aircraft.weight
            #"pre climb" equations
            
            thrust, aircraft_efficiency = propeller.prop_thrust_from_motor_power(max_power, calculate_air_density(altitude), speed)
            #print(thrust, 2)
            
            if not one_motor:
                thrust *= 2
            
            if speed > aircraft.climb_speed * 0.9:
                flaps = 10
            
            angle_of_attack = min(12 - climb_angle, 8)
            
            acceleration_x, acceleration_y, acceleration = calculate_takeoff_acceleration(aircraft, thrust, angle_of_attack, climb_angle, altitude, speed, flaps)
            
            speed_x += acceleration_x * time_step
            speed_y += acceleration_y * time_step
            speed += acceleration * time_step
            
            climb_angle = np.degrees(np.arctan(speed_y / speed_x))
            
            position += speed_x * time_step
            altitude += speed_y * time_step
            
            if first:
                first = False
            
            if speed >= aircraft.climb_speed:
                stage = 1
                acceleration_x = 0
                acceleration_y = 0
                acceleration = 0
                flaps = 0
                first = True
                
        
        elif stage == 1:      # Climb
            climb_angle = aircraft.climb_angle
            
            speed = aircraft.climb_speed
            speed_x = speed * cos(climb_angle)
            speed_y = speed * sin(climb_angle)
            
            position += (speed_x + windspeed) * time_step
            altitude += speed_y * time_step
            
            angle_of_attack = calculate_angle_of_attack(aircraft, climb_angle, altitude, speed, flaps)
            
            thrust = calculate_thrust(aircraft, climb_angle, altitude, speed, flaps)
            
            if first:
                aircraft_efficiency = propeller.calc_motor_operating_point(propeller.prop1, thrust/2, speed, calculate_air_density(altitude), 0.95, 0.9)[3]
                print("Climb:", aircraft_efficiency)
                first = False
            
            if altitude >= cruise_alt: #Om vi är över vår cruising altitude går vi över till cruise
                stage = 2
                first = True
        
        elif stage == 2:     # Cruise
            climb_angle = aircraft.cruise_angle
            
            speed = aircraft.cruise_speed
            speed_x = speed
            speed_y = 0
            
            position += (speed_x + windspeed) * time_step
            altitude += speed_y * time_step
            
            angle_of_attack = calculate_angle_of_attack(aircraft, climb_angle, altitude, speed, flaps)
            
            thrust = calculate_thrust(aircraft, climb_angle, altitude, speed, flaps)
            
            if first:
                aircraft_efficiency = propeller.calc_motor_operating_point(propeller.prop1, thrust/2, speed, calculate_air_density(altitude), 0.95, 0.9)[3]
                print("Cruise:", aircraft_efficiency)
                print(climb_angle)
                print(speed)
                print(thrust)
                print(aircraft_efficiency)
                first = False
            
            if total_distance + descent_distance_calc(aircraft,cruise_alt ) < position: #om vi har nått till det området när vi behöver stiga ner så går vi över till descent
                stage = 3
                first = True
                print(calculate_lift_coefficient(angle_of_attack, flaps), calculate_drag_coefficient(angle_of_attack, flaps), calculate_lift_coefficient(angle_of_attack, flaps)/calculate_drag_coefficient(angle_of_attack, flaps), angle_of_attack)
        
        elif stage == 3:     # Descent                
            if descent_stall == True:
                climb_angle = aircraft.cruise_angle
            
                speed = aircraft.cruise_speed
                speed_x = speed
                speed_y = 0
                
                angle_of_attack = calculate_angle_of_attack(aircraft, climb_angle, altitude, speed, flaps)
                
                thrust = calculate_thrust(aircraft, climb_angle, altitude, speed, flaps)
                
                time_stall += time_step
                
                if first:
                    aircraft_efficiency = propeller.calc_motor_operating_point(propeller.prop1, thrust/2, speed, calculate_air_density(altitude), 0.95, 0.9)[3]
                    print("Descent stall:", aircraft_efficiency)
                    print(climb_angle)
                    print(speed)
                    print(thrust)
                    print(aircraft_efficiency)
                    first = False
                
                if time_stall >= 45*60:
                    descent_stall = False
                    first = True
                    
            elif descent_stall == False:
                climb_angle = aircraft.descent_angle
            
                speed = aircraft.descent_speed
                speed_x = speed * cos(climb_angle)
                speed_y = speed * sin(climb_angle)
            
                position += (speed_x + windspeed) * time_step
                altitude += speed_y * time_step
            
                angle_of_attack = calculate_angle_of_attack(aircraft, climb_angle, altitude, speed, flaps)
                
                thrust = calculate_thrust(aircraft, climb_angle, altitude, speed, flaps)
                
                if first:
                    aircraft_efficiency = propeller.calc_motor_operating_point(propeller.prop1, thrust/2, speed, calculate_air_density(altitude), 0.95, 0.9)[3]
                    print("Descent:", aircraft_efficiency)
                    first = False
                
                if altitude < 1500 and time_stall <= 45*60:
                    descent_stall = True
                    first = True

        power_consumption = 30000 + energy_for_flight_phase(aircraft, altitude, climb_angle, speed ,stage, thrust, flaps, time_step) / (aircraft_efficiency * time_step)
        energy_consumption += power_consumption * time_step / 3600000
        
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
        
        aircraft_efficiency_list.append(aircraft_efficiency)
        
        if stage > 1 and altitude <= 1:
            flying = False
        
        if position >= runway and takeoff_calculation:
            
            return altitude
    
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
    
    plt.figure(figsize=(8, 5))
    plt.plot(position_list, altitude_list)
    plt.title("Altitude over distance")
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
    """
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, angle_of_attack_list)
    plt.title("AOA over time")
    plt.show()
    """
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, speed_x_list)
    plt.title("Ground speed over time")
    plt.show()
    
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, speed_list)
    plt.title("Speed over time")
    plt.show()
    """
    plt.figure(figsize=(8, 5))
    plt.plot(t_list, acceleration_list)
    plt.title("Acceleration over time")
    plt.show()
    """
    plt.figure(figsize=(8, 5))
    plt.plot(position_list, climb_angle_list)
    plt.title("Climb angle over distance")
    plt.show()

    """
    
    

def calculate_max_power(aircraft):
    def func(power):
        return prel_main(aircraft, power, 1100, True) - 15
    
    return fsolve(func, 2000000)[0]
    

#print("Max power:", calculate_max_power(lek_30))

#print(prel_main(lek_30, 0.01, 2300000, True))

prel_main(lek_30)

C_L = []
C_D = []
L_D = []

for i in range(11):
    print(f"L/D with AOA {i}:", calculate_lift_coefficient(i, 0) / calculate_drag_coefficient(i, 0))
    C_L.append(calculate_lift_coefficient(i, 0))
    C_D.append(calculate_drag_coefficient(i, 0))
    L_D.append(calculate_lift_coefficient(i, 0) / calculate_drag_coefficient(i, 0))

plt.figure(figsize=(8, 5))
plt.plot(range(11), L_D)
plt.title("")
plt.show()
    
"""
print("Thrust climb:")
print(calculate_thrust(lek_30, lek_30.climb_angle, 100, lek_30.climb_speed, 0)) 79%
print(calculate_thrust(lek_30, lek_30.climb_angle, 3000, lek_30.climb_speed, 0)) 79%
print("Thrust Cruise:")
print(calculate_thrust(lek_30, lek_30.cruise_angle, 3000, lek_30.cruise_speed, 0)) 86%
print("Thrust descent:")
print(calculate_thrust(lek_30, lek_30.descent_angle, 3000, lek_30.descent_speed, 0)) 79%
"""
