import random

class TrafficLight:
    def __init__(self, light_id:int, position_miles:float, cycle_duration: float = 60.0, green_duration: float = 30.0 , yellow_duration: float = 4.0, offset: float= 0.0): 
        #I initialize some base values since they will just be overriden by generate_random_cycle, but still useful if I need to create one light
        #Constructor for the traffic light
        self.light_id=light_id
        self.position_miles = position_miles
        self.cycle_duration = cycle_duration
        self.green_duration = green_duration
        self.yellow_duration = yellow_duration
        self.red_duration = cycle_duration - green_duration - yellow_duration #since I pass in green and yellow duration, red will always be the total cycle minus those
        self.offset = offset

    def generate_random_cycle(self): #helper function to create a random cycle for each light
        self.cycle_duration = random.uniform(55,75) #documentation for these numbers in documentation.txt
        self.green_duration = self.cycle_duration*0.5 #green is about half the cycle
        self.yellow_duration = 4.0 #yellow fixed to 4 seconds
        self.red_duration = max(0.0, self.cycle_duration - self.green_duration - self.yellow_duration) #added max being 0 to protect against negative edgecases

    def calculate_offset(self, steady_speed_mph: float):
        #I calculate offset by using the time it would take a steady driver to reach the lights position
        #This is really just used to create green wave possibility for the steady driver, whereas a speeder wouldnt have that
        steady_ftps = steady_speed_mph * 1.46667
        base_offset = (self.position_miles*5280) / steady_ftps
        return base_offset
    
    def assign_offset_to_light(self, steady_speed_mph: float, green_wave_probability: float=random.uniform(0.45, 0.55)):
        #I created this function to serve the purpose that steady drivers wont always hit a green wave
        #In this case, 45% of the driving should be a green wave
        if random.uniform(0,1) < green_wave_probability: 
            self.offset = self.calculate_offset(steady_speed_mph) 
        else:
            self.offset = random.uniform(0,self.cycle_duration)

    def get_light_state(self, current_time_elapsed):
        time = (current_time_elapsed - self.offset) % self.cycle_duration
        if(time<self.green_duration):
            return "green"
        elif (time<self.green_duration + self.yellow_duration):
            return "yellow"
        else:
            return "red"
            
    