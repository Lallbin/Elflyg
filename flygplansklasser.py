class Aircraft:
    def __init__(self, weight, ref_area, cruise_speed, climb_speed, descent_speed, takeoff_speed,climb_angle, cruise_angle, descent_angle, max_motor_power, runway_length):
        self.weight = weight
        self.ref_area = ref_area
        self.cruise_speed = cruise_speed
        self.climb_speed = climb_speed
        self.descent_speed = descent_speed
        self.climb_angle = climb_angle
        self.cruise_angle = cruise_angle
        self.descent_angle = descent_angle
        self.max_motor_power = max_motor_power
        self.runway = runway_length
        self.takeoff_speed = takeoff_speed



