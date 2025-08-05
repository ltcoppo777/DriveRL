import random

class Driver:
    '''The driver has speed, position, and time tracking'''

    def __init__(self, driver_id: str, speed_limit_mph: float, driver_style: str="safe"):
        self.driver_id = driver_id
        self.driver_style = driver_style
        self.speed_limit_mph = speed_limit_mph
        self.speed_mph = self.determine_speed()
        self.driver_type = self.determine_driver_type()
        self.position_miles = 0.0
        self.time_elapsed_sec = 0.0
        self.red_light_count = 0

    def determine_speed(self):
        if self.driver_style == "safe":
            speed = self.speed_limit_mph
        elif self.driver_style == "realistic":
            speed = self.speed_limit_mph + random.uniform(5,10) #realistically speeders go 5-10 above limit
        elif self.driver_style == "aggressive":
            speed = self.speed_limit_mph + random.uniform(11,16) #aggressive speeders 11-16 above the limit
        print(f"Driver style: {self.driver_style}, Speed: {speed:.1f}")  #Debug line
        return speed

    def determine_driver_type(self):
        if self.driver_style=="realistic" or self.driver_style=="aggressive":
            return "speeder"
        else:
            return "steady"
        
    

    def travel_to_position (self, target_position: float, override_speed_mph: float = None): #this function will traverse my driver to the position, calculating time elapsed etc.
        if target_position <= self.position_miles: #edge case, where the drivers position is somehow past the target position
            self.position_miles += 0 #does nothing, but this is what I want to portray
            self.time_elapsed_sec+=0 #same here
            return 0.0
        
        #to prevent divide zero error
        if override_speed_mph is not None:
            speed_to_use = override_speed_mph
        else:
            speed_to_use = self.speed_mph
        
        if speed_to_use < 0.1:
            speed_to_use = 0.1

        #the real function
        distance_to_travel = target_position-self.position_miles
        travel_time_seconds = (distance_to_travel/speed_to_use)*3600 #3600 converts hours to seconds

        self.position_miles = target_position
        self.time_elapsed_sec+= travel_time_seconds
        return travel_time_seconds 
    
    def wait_at_light(self, wait_time:float): #Penalty for hitting a red light for both drivers
        self.time_elapsed_sec += wait_time

    def get_acceleration_penalty_per_stop(self): #When the drivers hit a red, or stop, they get this penalty
        speed_mps = self.speed_mph * 0.44704 #My documentation for my data is under my documentation text file

        if self.driver_type == "speeder":
            acceleration = 3.25 #m/s², a bit slow due to braking 
            inefficiency_penalty = 5  #second delay, poor traction, brakes, etc.
        else:
            acceleration = 2.5  #m/s²
            inefficiency_penalty = 2  #seconds

        acceleration_time = speed_mps / acceleration
        return acceleration_time + inefficiency_penalty
    
    def reset(self): #resets the driver
        self.position_miles = 0.0
        self.time_elapsed_sec = 0.0


        