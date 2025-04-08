from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt

class Propeller:
    def __init__(self, efficiency_data, thrust_coeff_data,power_coeff_data, pitch_angles,start_advance_ratio,diameter):
        self.efficiency_data=efficiency_data
        self.thrust_coeff_data=thrust_coeff_data
        self.power_coeff_data=power_coeff_data
        self.pitch_angles=pitch_angles
        self.start_advance_ratio=start_advance_ratio
        self.diameter=diameter
#verktyg: https://plotdigitizer.com/app        
#efficiency_data        
prop_1_eff_x_15 = [0.00536, 0.10184, 0.23476, 0.31623, 0.40842, 0.47274, 0.53277, 0.60781, 0.6657, 0.70214, 0.73216, 0.75145, 0.76646, 0.77718, 0.79648, 0.80934]
prop_1_eff_y_15 = [-0.00212, 0.23718, 0.47012, 0.58024, 0.67129, 0.73271, 0.77082, 0.80682, 0.81529, 0.80259, 0.77294, 0.73271, 0.66706, 0.56965, 0.44047, 0.01271]
prop_1_eff_x_20 = [0.00643, 0.06217, 0.13507, 0.20796, 0.31302, 0.42021, 0.53813, 0.64747, 0.73538, 0.82971, 0.91547, 0.96049, 0.97764, 1.00123, 1.02266, 1.03338, 1.03982]
prop_1_eff_y_20 = [0.00212, 0.11012, 0.24353, 0.35576, 0.49765, 0.62047, 0.71576, 0.78353, 0.82165, 0.85129, 0.83435, 0.80047, 0.756, 0.612, 0.39812, 0.19482, 0.02965]
prop_1_eff_x_25 = [0.00429, 0.25513, 0.34946, 0.44165, 0.55743, 0.66248, 0.75253, 0.91761, 1.0441, 1.11914, 1.18989, 1.23277, 1.24992, 1.28423]
prop_1_eff_y_25 = [-0.00424, 0.29224, 0.41718, 0.54424, 0.65012, 0.73059, 0.77929, 0.84706, 0.86824, 0.85341, 0.792, 0.70306, 0.58235, 0.00847]
prop_1_eff_x_30 = [0, 0.24012, 0.67963, 0.73966, 0.8147, 0.87902, 0.9755, 1.08484, 1.20276, 1.30352, 1.39357, 1.45789, 1.48147, 1.50291, 1.53292, 1.55008]
prop_1_eff_y_30 = [-0.00212, 0.19906, 0.62894, 0.68188, 0.73906, 0.77294, 0.80894, 0.84494, 0.86824, 0.86824, 0.83859, 0.78141, 0.72, 0.63529, 0.36424, 0.00635]
prop_1_eff_x_35 = [0.01072, 0.92404, 0.99265, 1.05697, 1.15345, 1.23063, 1.33354, 1.42787, 1.48361, 1.55865, 1.61868, 1.67871, 1.71302, 1.75804, 1.81164, 1.83093]
prop_1_eff_y_35 = [0.00424, 0.69035, 0.73694, 0.76871, 0.79835, 0.82165, 0.83859, 0.84918, 0.85553, 0.85553, 0.83647, 0.792, 0.74541, 0.63318, 0.31341, 0.00847]
prop_1_eff_x_40 = [-0.00214, 1.18989, 1.29066, 1.40214, 1.54793, 1.66156, 1.78806, 1.88668, 1.97458, 2.03247, 2.08606, 2.13538, 2.1611, 2.18683]
prop_1_eff_y_40= [-0.00212, 0.70729, 0.756, 0.79835, 0.828, 0.84494, 0.84494, 0.81953, 0.76024, 0.69671, 0.57812, 0.396, 0.22659, 0.01059]
prop_1_eff_x_45= [0.00429, 1.12343, 1.2928, 1.40858, 1.51363, 1.63155, 1.75804, 1.90597, 2.06463, 2.21041, 2.33691, 2.4441, 2.50842, 2.56631, 2.59204, 2.61991, 2.64349]
prop_1_eff_y_45= [0, 0.54635, 0.62682, 0.69035, 0.73482, 0.77718, 0.80682, 0.83224, 0.83435, 0.80259, 0.73694, 0.65012, 0.56541, 0.44259, 0.34306, 0.19906, 0.01482]
#prop thrust coefficient data
prop_1_thrust_x_15= [-0.00422, 0.05913, 0.12459, 0.21961, 0.28296, 0.37164, 0.48145, 0.57225, 0.68627, 0.79608]
prop_1_thrust_y_15= [0.15915, 0.15416, 0.14627, 0.13505, 0.12425, 0.10742, 0.08498, 0.06171, 0.0347, 0.00436]
prop_1_thrust_x_20= [0.00211, 0.12036, 0.22805, 0.28296, 0.34208, 0.41388, 0.48989, 0.64615, 0.84465, 1.05158]
prop_1_thrust_y_20= [0.18699, 0.18408, 0.1793, 0.17536, 0.16954, 0.15811, 0.14294, 0.10762, 0.05859, 0.00083]
prop_1_thrust_x_25= [0, 0.13514, 0.22805, 0.3463, 0.48989, 0.55113, 0.63348, 0.91644, 1.18673, 1.28175]
prop_1_thrust_y_25= [0.19572, 0.19302, 0.19177, 0.19073, 0.18512, 0.1793, 0.16351, 0.09807, 0.02701, 0.00083]
prop_1_thrust_x_30= [0.00845, 0.42232, 0.50045, 0.58703, 0.64615, 0.69683, 0.73695, 0.77285, 0.82564, 0.8911, 1.03258, 1.21629, 1.41056, 1.5457]
prop_1_thrust_y_30= [0.20777, 0.19883, 0.19655, 0.19613, 0.19468, 0.19219, 0.18949, 0.18429, 0.17702, 0.16435, 0.13422, 0.09412, 0.03968, 0.00145]
prop_1_thrust_x_35= [0.00211, 0.13725, 0.31674, 0.454, 0.54691, 0.61659, 0.6905, 0.76652, 0.86365, 0.94389, 1.00302, 1.06425, 1.12971, 1.22896, 1.49502, 1.83922]
prop_1_thrust_y_35= [0.21525, 0.21421, 0.2113, 0.20735, 0.2032, 0.19863, 0.1953, 0.19302, 0.19322, 0.19011, 0.18491, 0.17702, 0.16642, 0.14772, 0.08685, 0.00104]
prop_1_thrust_x_40= [0, 0.16471, 0.38009, 0.54902, 0.6546, 0.74118, 0.84676, 0.93544, 1.00935, 1.09593, 1.17406, 1.23318, 1.31976, 1.41267, 1.50347, 1.60483, 1.78643, 2.04404, 2.2]
prop_1_thrust_y_40= [0.21857, 0.21816, 0.21691, 0.21504, 0.21234, 0.2086, 0.2032, 0.19863, 0.19593, 0.19551, 0.19468, 0.19239, 0.18533, 0.17349, 0.15853, 0.13609, 0.09537, 0.0374,0]
prop_1_thrust_x_45= [0.00211, 0.1098, 0.28084, 0.49201, 0.65249, 0.79397, 0.93756, 1.04103, 1.16772, 1.27541, 1.381, 1.46968, 1.56682, 1.68718, 1.80543, 2.00603, 2.62896]
prop_1_thrust_y_45= [0.22979, 0.23, 0.22917, 0.22543, 0.22023, 0.21421, 0.20631, 0.20029, 0.19551, 0.19364, 0.19302, 0.19115, 0.18741, 0.1766, 0.15915, 0.12466, 0.00125]

#prop power coefficient
prop_1_power_x_15= [0, 0.14440557685526167, 0.2594406114647591, 0.35979024050329156, 0.45524479410620566, 0.5409091072058284, 0.6486013942138152]
prop_1_power_y_15= [0.07350786696251305, 0.07287959852830651, 0.06848168497683459, 0.060000009347007145, 0.045863883297294794, 0.028900532037639995, 0.001884816806628273]
prop_1_power_x_20=  [0.0048950754356180725, 0.16153847532800839, 0.28636366080874226, 0.3842657073134378, 0.4821678434501888, 0.5678321565498109, 0.6437062291461417, 0.8370630085178623]
prop_1_power_y_20= [0.11811519038337724, 0.11717278198006306, 0.11497383670833587, 0.10837697788513682, 0.09518326023873866, 0.08073299421991857, 0.06376964296026377, 0.001884816806628273]
prop_1_power_x_25= [-0.00244758253383696, 0.20314684061090127, 0.354895075435618, 0.4503496290385321, 0.5604894985803559, 0.6534965592814889, 0.7538460986879658, 0.8590909824262271, 0.9643356869003773, 1.0377622665949264]
prop_1_power_y_25= [0.17528796876843747, 0.16649215892150684, 0.16020944006741544, 0.15424084967842286, 0.14167540046623112, 0.12534032914479162, 0.10083771065862356, 0.06471205136357795, 0.027329843696110516, 0.001256559876430689]
prop_1_power_x_30= [-0.007342657969455033, 0.217832156549811, 0.3328671911593084, 0.41118884628947616, 0.4944055768552616, 0.5776223970531029, 0.6951048349323262, 0.6951048349323262, 0.8003497186705875, 0.9055944231447377, 1.0206294577542354, 1.1479021361367507, 1.2482518548073385]
prop_1_power_y_30= [0.26638743816879856, 0.2378010461002662, 0.22586387682628986, 0.22020942640640492, 0.21675393276225594, 0.21015707393905686, 0.1928795827102944, 0.1928795827102944, 0.17403142614802009, 0.14607331401770304, 0.10617802110940082, 0.04712042016570776, 0.002198968279744783]
prop_1_power_x_35= [0, 0.14930074192293527, 0.35244758253383657, 0.4625874520756607, 0.5506993477091198, 0.6437062291461417, 0.7048951650676735, 0.8101398695418237, 0.9594405218327041, 1.081818214411656, 1.1968532490211543, 1.3486015734779262, 1.4856644027316777]
prop_1_power_y_35= [0.3310994809043699, 0.31853404032018484, 0.2974869097261613, 0.2846073378008752, 0.2773822105434696, 0.27392670539531183, 0.2679581265103281, 0.2538220004606157, 0.22083770634462024, 0.18471205280157907, 0.13947645519450394, 0.06879582494594223, 0.001884816806628273]
prop_1_power_x_40= [0, 0.27412592740366915, 0.42587416222838587, 0.53601403177021, 0.6167832694342144, 0.6902098491287637, 0.7685314146268756, 0.8664336403956822, 0.9423077129920125, 1.0108393068829986, 1.0842658865775483, 1.1454546432349693, 1.25069934770912, 1.4293708111419299, 1.7916085445470036]
prop_1_power_y_40= [0.3845026199241691, 0.37916230947339186, 0.3731937190843993, 0.36471204345457187, 0.35623036782474443, 0.34743455222580943, 0.34083770490661913, 0.33706807129336247, 0.3317277493385764, 0.323246073708749, 0.310994764465665, 0.2962303584777373, 0.2610471277180213, 0.18722513229040946, 0.00314135367504133]
prop_1_power_x_45= [0.0024474929017814463, 0.15174823482471672, 0.28636366080874226, 0.4625874520756607, 0.6192307623359955, 0.7905593885352407, 0.9251749041513214, 1.0132867997847808, 1.096503530350566, 1.1772727680145703, 1.2555945127767931, 1.3828671911593085, 1.5444056664873171, 1.7548952546997287, 1.872377782211008, 1.9727273216174845, 2.0926575212946554, 2.156293770853858]
prop_1_power_y_45= [0.4821989553377349, 0.4781151831933717, 0.4727748727425944, 0.4564397899171461, 0.4375916247268652, 0.4212565476534213, 0.40994764681365137, 0.4046073363628741, 0.4042931963937665, 0.40115183121471626, 0.3910994787473682, 0.35937173300379466, 0.30785341079062367, 0.22397906001966153, 0.15958114862519124, 0.10806281490801149, 0.03832461607078153, 0.0031413766830589622]


#data för prop1 är hämtad från "naca-report-640" och gäller propellern "Clark Y 4 section 4 blade"
prop1=Propeller([[prop_1_eff_x_15,prop_1_eff_y_15],[prop_1_eff_x_20,prop_1_eff_y_20],[prop_1_eff_x_25,prop_1_eff_y_25],
                       [prop_1_eff_x_30,prop_1_eff_y_30],[prop_1_eff_x_35,prop_1_eff_y_35],[prop_1_eff_x_40,prop_1_eff_y_40],[prop_1_eff_x_45,prop_1_eff_y_45]],  
        [[prop_1_thrust_x_15,prop_1_thrust_y_15],[prop_1_thrust_x_20,prop_1_thrust_y_20],[prop_1_thrust_x_25,prop_1_thrust_y_25],[prop_1_thrust_x_30,prop_1_thrust_y_30],
         [prop_1_thrust_x_35,prop_1_thrust_y_35],[prop_1_thrust_x_40,prop_1_thrust_y_40],[prop_1_thrust_x_45,prop_1_thrust_y_45]],
        [[prop_1_power_x_15,prop_1_power_y_15],[prop_1_power_x_20,prop_1_power_y_20],[prop_1_power_x_25,prop_1_power_y_25],[prop_1_power_x_30,prop_1_power_y_30],
         [prop_1_power_x_35,prop_1_power_y_35],[prop_1_power_x_40,prop_1_power_y_40],[prop_1_power_x_45,prop_1_power_y_45]],
        [15,20,25,30,35,40,45], 
        0.5,
        13  #Anges i fot
           )


def calc_prop_efficiency(propeller, aircraft_speed, advance_ratio, current_pitch_angle): #Räknar ut bästa pitchvinkel,propellerhastighet samt den verkningsgrad som erhålles
      
    
    
    pitch_angle_step_size= (propeller.pitch_angles[1] - propeller.pitch_angles[0] )
    index=int( (current_pitch_angle-propeller.pitch_angles[0])/pitch_angle_step_size )
    
    
    efficiency= np.interp(advance_ratio, propeller.efficiency_data[index][0],propeller.efficiency_data[index][1])  
    prop_rps= aircraft_speed/ (propeller.diameter*advance_ratio) # prop_rps är propellerns varvtal per sekund     
    
    return prop_rps, efficiency

def calc_coefficients(propeller, advance_ratio, current_pitch_angle):  # Räknar ut thrust_coefficient givet advance ratio och tillhörande pitch-vinkel
    
    pitch_angles= propeller.pitch_angles
    pitch_angle_step_size= (propeller.pitch_angles[1] - propeller.pitch_angles[0] )
    index=int( (current_pitch_angle-propeller.pitch_angles[0])/pitch_angle_step_size )
    

    thrust_coefficient= np.interp(advance_ratio, propeller.thrust_coeff_data[index][0], propeller.thrust_coeff_data[index][1])
    power_coefficient=np.interp(advance_ratio, propeller.power_coeff_data[index][0], propeller.power_coeff_data[index][1])
    return thrust_coefficient, power_coefficient


def calc_prop_thrust( propeller, thrust_coefficient, prop_rps, rho):       #Räknar ut den thrust som erhålles i newton
    thrust_in_lb=thrust_coefficient*(prop_rps**2)*rho*propeller.diameter**4
    thrust_in_N=thrust_in_lb*4.44822  #skalfaktorn kommer från att thrust koefficienten ger thrust i lb
    return thrust_in_lb #OBS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def calc_motor_electric_power_req(propeller, thrust, prop_rps, aircraft_speed, motor_efficiency, prop_efficiency,thrust_coefficient, power_coefficient ):  #Räknar den elektriska effekt motorn måste leverera
    
    forward_flight_motor_electric_power =  aircraft_speed*thrust/ (motor_efficiency*prop_efficiency)
    
    static_flight_motor_electric_power= thrust*prop_rps*propeller.diameter*(power_coefficient/thrust_coefficient)/motor_efficiency
    
    ## Om flygplanets hastighet är mindre än 82 feet/second beräknar vi en linjärkombination av static thrust och forward flight thrust
    # Om hastigheten är större än 82 feet/second använder vi bara forward flight thrust-beräkningen. 
    
    linear_weight= (static_forward_flight_threshold-aircraft_speed) / static_forward_flight_threshold 
    
    if aircraft_speed>static_forward_flight_threshold:
        motor_electric_power=forward_flight_motor_electric_power
        
    else:
        motor_electric_power= (static_flight_motor_electric_power*(1-linear_weight) + forward_flight_motor_electric_power * linear_weight)
        
    return motor_electric_power*1.355 ## konvertering från pound foot/second till Joule/sekund
     
def calc_motor_electric_torque(electric_power, prop_rps ): #Räknar ut det vridmoment motorn måste klara av att leverera
    
    omega= 2*3.1415*prop_rps
    
    motor_torque= electric_power/omega
    
    return motor_torque 
    
def find_advance_ratio_for_current_pitch_angle(propeller, F_required, aircraft_speed, current_pitch_angle, rho ):
    
    
    
    def thrust_diff_func(advance_ratio):  ## Denna funktion används i sökalgorimen nedan för att räkna ut differensen mellan sökt och nuvarande thrust
        
        
        prop_rps, prop_efficiency = calc_prop_efficiency(propeller, aircraft_speed, advance_ratio, current_pitch_angle) 
        thrust_coefficient,power_coefficient =calc_coefficients(propeller,advance_ratio, current_pitch_angle)
        
        prop_thrust= calc_prop_thrust(propeller, thrust_coefficient, prop_rps, rho) 

        return prop_thrust-F_required , thrust_coefficient, power_coefficient
     
          
    ### Koden nedan är en sökalgoritm som stegar sig fram till en advance ratio för den givna pitch_anglen till dess att thrust-kravet uppfylls___________________________________________
    
    threshold=50
    count=0
    thrust_diff=threshold*2
    
     
    advance_ratio=propeller.start_advance_ratio
    search_step=0.05
    current_iteration_status=-1
    last_iteration_status=-1
    
    
    while abs(thrust_diff)>threshold:
        
      thrust_diff, thrust_coefficient, power_coefficient =thrust_diff_func(advance_ratio) 
     
      if abs(thrust_diff)>threshold: 
        if thrust_diff>0:
            advance_ratio= advance_ratio+search_step  #Istället för att addera 0.01 måste det göras proportionerligt mot rotationshastigheten
            last_iteration_status=current_iteration_status
            current_iteration_status=1
        elif thrust_diff<0:
            advance_ratio=advance_ratio - search_step
            last_iteration_status=current_iteration_status
            current_iteration_status=0
            
      if current_iteration_status !=last_iteration_status :#Om den resulterande thrusten hoppar runt, halvera söksteget
           search_step=search_step/2   
           
      count+=1
    
    ### Slut på sökalgoritm ____________________________________________________________________________________________________       

    return advance_ratio,thrust_coefficient, power_coefficient
    
def calc_motor_operating_point(propeller, F_required, aircraft_speed, rho, motor_efficiency,prop_tip_speed_cut_off): # Moderfunktion som samlar alla andra funktioner för att beräkna en arbetspunkt för motorn.
    
    F_required=F_required/4.45 # Omvandling från Newton till lb
    rho=rho/515.4 # omvandling från kg/m^3 till slug/ft^3. standardvärde i kg/m^3 är ca 1.2
    aircraft_speed=aircraft_speed*3.28 # omvandling från m/s till fot/sekund
    
    global static_forward_flight_threshold
    
    static_forward_flight_threshold=25*3.32
    
    #1: Nedan loop finner en arbetspunkt för propellern för varje pitch-angle, som uppfyller thrustkravet. Enbart den arbetspunkt med bäst verkningsgrad sparas.
    

    lowest_motor_electric_power=1000000000
    highest_efficiency=0
    saved_prop_efficiency=None
    saved_prop_rps=0
    
    for current_pitch_angle in propeller.pitch_angles: 
        
        advance_ratio, thrust_coefficient, power_coefficient = find_advance_ratio_for_current_pitch_angle(propeller, F_required, aircraft_speed, current_pitch_angle, rho ) # Finn J som uppfyllter F_required

        prop_rps, prop_efficiency = calc_prop_efficiency(propeller, aircraft_speed, advance_ratio, current_pitch_angle)  
        
        prop_tip_speed= ((3.1415*propeller.diameter*prop_rps)**2 + (aircraft_speed)**2)**0.5  # propellerns spetshastighet är normen av flygplanets hastighet och propellerns rotationshastighet vid spetsen
        
        ## om flygplanets hastighet är mindre än 25 m/s används en linjär viktining av den effekt som fås från static thrust och forward thrust beräkningarna. 
        
        
        #print(prop_efficiency,advance_ratio,current_pitch_angle,prop_rps,thrust_coefficient,prop_tip_speed)
        
        if aircraft_speed>static_forward_flight_threshold:
        
            if prop_efficiency>highest_efficiency and prop_tip_speed<343*3.28*prop_tip_speed_cut_off:           #spara enbart arbetspunkten om den har högst verkningsgrad hittills, och propellertoppen ej går för fort!
                highest_efficiency=prop_efficiency
                saved_prop_efficiency=prop_efficiency
                saved_prop_rps=prop_rps
                saved_pitch_angle=current_pitch_angle
                saved_advance_ratio=advance_ratio
                saved_thrust_coefficient=thrust_coefficient
                saved_power_coefficient=power_coefficient
                
        else:
            motor_electric_power= calc_motor_electric_power_req(propeller, F_required, prop_rps, aircraft_speed, motor_efficiency, prop_efficiency, thrust_coefficient,power_coefficient) 
        
            if motor_electric_power<lowest_motor_electric_power and prop_tip_speed<343*3.28*prop_tip_speed_cut_off:
                lowest_motor_electric_power=motor_electric_power
                saved_prop_rps=prop_rps
                saved_pitch_angle=current_pitch_angle
                saved_advance_ratio=advance_ratio
                saved_thrust_coefficient=thrust_coefficient
                saved_power_coefficient=power_coefficient
                
                
                
                
            
        
        
    
    # 4: Nu kan vi beräkna motorns elektriska effekt _________________ (propeller, thrust, prop_rps, aircraft_speed, motor_efficiency, prop_efficiency,thrust_coefficient, power_coefficient )
    
    if aircraft_speed>static_forward_flight_threshold:
        lowest_motor_electric_power= calc_motor_electric_power_req(propeller, F_required, saved_prop_rps, aircraft_speed, motor_efficiency, saved_prop_efficiency, saved_thrust_coefficient,saved_power_coefficient) 
        
    
    
    # 5: Slutligen kan vi beräkna motorns vridmoment ________________
    
    motor_torque= calc_motor_electric_torque(lowest_motor_electric_power,saved_prop_rps)
    
    
    return lowest_motor_electric_power, motor_torque, saved_prop_rps, saved_prop_efficiency, saved_advance_ratio, saved_pitch_angle
       
    
    
#print(calc_motor_operating_point(6000,78,1.2,0.95)) 


aircraft_speed=40  #anges här i m/s. OMvandlas till feet/s i funktionen som kallas nedan. 
F_required=35000   #Anges här i Newton. Omvandlas till lb i funktionen nedan 


rho=1.2 # Anges i kg/m^3 och omvandlas i funktionen nedan till slug/ft^3
motor_efficiency=0.95
prop_tip_speed_cut_off=0.9 # Anger max tillåten propellerhastighet, definierad som andel av ljudets hastighet som propellerns topp rör sig i.  




#print(calc_motor_operating_point(prop1, F_required, aircraft_speed, rho, motor_efficiency,prop_tip_speed_cut_off))

# 97 m/s 
# 12 kN


    
def plot1(propeller):    
  for data in propeller.efficiency_data: 
      x=np.array(data[0])
      y=np.array(data[1])
      plt.plot(x,y)
    
  plt.show()
  



def prop_thrust_from_motor_power(motor_power, rho, aircraft_speed):
    propeller=prop1
    motor_efficiency=0.95
    prop_tip_speed_cut_off=0.9
    advance_ratio=0
    prop_rps=15
    start_advance_ratio=propeller.start_advance_ratio
    prop_tip_speed= ((prop_rps*np.pi*propeller.diameter)**2 + aircraft_speed**2)**0.5
    motor_efficiency=0.95
    
    aircraft_speed=max(5,aircraft_speed)
    
    saved_thrust=0

    def get_motor_power_diff(current_advance_ratio):
    
    
        static_forward_flight_threshold=25
        prop_rps= aircraft_speed*3.28 / (current_advance_ratio*propeller.diameter)
        thrust_coefficient, power_coefficient =calc_coefficients(propeller,current_advance_ratio,blade_pitch)
        prop_tip_speed= ((prop_rps*np.pi*propeller.diameter/3.28)**2 + aircraft_speed**2)**0.5
        
        thrust_coefficient=max(0.0001,thrust_coefficient)
        
        if prop_tip_speed>343*prop_tip_speed_cut_off or current_advance_ratio<0:
            penalty=20000000
            
        else:
            penalty=0
                
        
        ## Alla enheter nedan är metriska, eller konverteras till metrisk enhet med konverteringsfaktor som syns i koden nedan######
        
        
        current_thrust= thrust_coefficient*0.002328*prop_rps**2*propeller.diameter**4*4.45   
        
        static_motor_power= current_thrust* (power_coefficient/thrust_coefficient)*prop_rps*propeller.diameter/3.28
            
        forward_flight_power= aircraft_speed*current_thrust/( motor_efficiency*max(0.001,calc_prop_efficiency(propeller,aircraft_speed,current_advance_ratio,blade_pitch)[1]))
        
        linear_weight= (static_forward_flight_threshold-aircraft_speed) / static_forward_flight_threshold 
        
        
        if aircraft_speed> static_forward_flight_threshold:
            
            current_motor_power=forward_flight_power
        else:
            current_motor_power=forward_flight_power*(1- linear_weight) + static_motor_power* linear_weight
        
        
        
        
        
        return  current_motor_power - motor_power +penalty
    
    def get_thrust_from_motor_power():
        
        static_forward_flight_threshold=25
        
        prop_rps= aircraft_speed*3.28 / (advance_ratio*propeller.diameter)
        
        thrust_coefficient, power_coefficient =calc_coefficients(propeller,advance_ratio,blade_pitch)
        prop_efficiency=calc_prop_efficiency(propeller,aircraft_speed,advance_ratio,blade_pitch)[1]
        
        static_thrust= motor_efficiency*(thrust_coefficient/power_coefficient)*motor_power/ ( prop_rps*propeller.diameter)*4.45
        
        forward_flight_thrust= prop_efficiency*motor_power*motor_efficiency/aircraft_speed
        
        
        linear_weight= (static_forward_flight_threshold-aircraft_speed) / static_forward_flight_threshold 
        
        
        if aircraft_speed> static_forward_flight_threshold:
            
            current_motor_power=forward_flight_thrust
        else:
            current_motor_power=forward_flight_thrust*(1- linear_weight) + static_thrust* linear_weight
        
        return thrust_coefficient*propeller.diameter**4*prop_rps**2*0.002328*4.45 ,prop_rps,prop_efficiency
        
        
         
    
    for blade_pitch in propeller.pitch_angles:
        
        advance_ratio = fsolve(get_motor_power_diff,start_advance_ratio)[0]
        
        current_thrust,prop_rps,prop_efficiency= get_thrust_from_motor_power()
        
        
        #current_thrust= prop_efficiency*motor_efficiency*motor_power/aircraft_speed
        
        #print("blade angle:", blade_pitch, "advance ratio: ", advance_ratio,"prop rps:",prop_rps, "prop eff:",prop_efficiency)
        
        if current_thrust>saved_thrust:
            saved_thrust=current_thrust
            
        #print(current_thrust)
        
        
        
            

            
    return saved_thrust
        

print(prop_thrust_from_motor_power(8000000,1.2,50))

def plot2():
    x=0
    datalistx=[]
    datalisty=[]
    while x<100:
        datalisty.append(prop_thrust_from_motor_power(2300000,1.2,x))
        datalistx.append(x)
        x+=1
        
        
    x=np.array(datalistx)
    y=np.array(datalisty)
    plt.plot(x,y)
        
    plt.show()
    






    
    
    
    
    
    
    
    
    
    
    
    








