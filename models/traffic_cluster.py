from models.driver import Driver

class TrafficCluster:
    def __init__(self, cluster_id: str, start_position_miles: float, end_position_miles: float, slowdown_speed: float, deceleration_rate: float):
        self.cluster_id = cluster_id
        self.start_position_miles = start_position_miles
        self.end_position_miles = end_position_miles
        self.slowdown_speed = slowdown_speed
        self.deceleration_rate = deceleration_rate

    def is_driver_in_cluster(self, driver_position_miles:float):
        if(driver_position_miles>=self.start_position_miles and driver_position_miles<=self.end_position_miles):
            return True
        else:
            return False
        
    def apply_cluster_effect(self, driver):
        driver.travel_to_position(self.start_position_miles)


        driverSpeed = driver.speed_mph
        speed_mps = driverSpeed * 0.44704 #For this logic, I used the same documentation as my acceleration logic in models.driver.get_acceleration_penalty_per_stop
        

        if driver.driver_type == "speeder":
            deceleration = 3.5  #m/s², 
            inefficiency_penalty = 8 #seconds
        else:
            deceleration = 2.5  #m/s²
            inefficiency_penalty = 2  #seconds

        #Calculating time taken to decelerate
        deceleration_time = speed_mps / deceleration
        total_penalty = deceleration_time + inefficiency_penalty

        #Applys the penalty for decelerating
        driver.wait_at_light(total_penalty)

        #Travels through the cluster at the reduced speed
        driver.travel_to_position(self.end_position_miles, override_speed_mph=self.slowdown_speed)

        #Have to treat clusters the same as a red light, you stop. Therefore, you need to accelerate after one, so I call the acceleration penalty once again from models.driver
        acceleration_penalty = driver.get_acceleration_penalty_per_stop()
        driver.wait_at_light(acceleration_penalty)



