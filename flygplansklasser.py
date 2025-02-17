class Aircraft:
    def __init__(self, weight, ref_area, cruise_speed, climb_angle, cruise_angle, descent_angle, propeller_efficiency):
        self.weight = weight
        self.ref_area = ref_area
        self.cruise_speed = cruise_speed
        self.climb_angle = climb_angle
        self.cruise_angle = cruise_angle
        self.descent_angle = descent_angle
        self.propeller_efficiency = propeller_efficiency


class ref_ES19:
    weight = 8616 #kg
    BatteryWeight = 2400 #kg
    totalWeight = weight + BatteryWeight #kg
    reference_area = 37.7 #m^2
    CruisingSpeed = 94 #m/s
    ClimbingSpeed = 92 #m/s
    DescentSpeed = 79 #m/s
    ClimbGamma = 4 #degrees
    CruiseGamma = 0 #degrees
    DescentGamma = -3 #degrees
    AngelOfAttack = "dont know angle of attack yet"

class ref_ES30:
    reference_area = 42     # (m^2)
    weight = 16000          # (kg) maximum take of weight 20-21 ton
    BatteryWeight = 50000   # kg
    TotalWeight = weight + BatteryWeight
    CruisingSpeed = 97    # (m/s)
    ClimbingSpeed = "dont know climbing speed yet"
    DescentSpeed = "dont know descent speed yet"
    ClimbGamma = "dont know climb gamma yet"
    CruiseGamma = 0 #degrees
    DescentGamma = "dont know descent gamma yet"
    AngelOfAttack = "dont know angle of attack yet"
  


