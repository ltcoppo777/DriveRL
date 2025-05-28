from models.driver import Driver
from models.traffic_light import TrafficLight
from utils.traffic_utils import time_until_green
from models.traffic_cluster import TrafficCluster
import random 


class Simulator:
    def __init__(self, total_distance, num_lights, speed_limit, steady_style="safe", speeder_style="aggressive"):
        self.total_distance = total_distance
        self.num_lights = num_lights

        self.steady_driver = Driver("driver1", speed_limit, driver_style=steady_style)
        self.speeder_driver = Driver("driver2", speed_limit, driver_style=speeder_style)
        
    def generate_traffic_lights(self):
        space_between_lights = self.total_distance / (self.num_lights + 1) #adding +1 so that I dont have a light right at position 0
        self.traffic_lights = []
        for x in range(self.num_lights):
            position = (x+1) * space_between_lights #since I added the +1, I calculate position by x+1
            position_randomness = position + random.uniform((-0.15*position),(0.15*position))
            light_id = x+1
            position_miles = position_randomness

            #Create an instance for my light
            light = TrafficLight(light_id, position_miles)
            light.generate_random_cycle() #generate the cycle
            light.assign_offset_to_light(self.steady_driver.speed_mph) #adjust the cycle to the steady driver
            self.traffic_lights.append(light) #add the light to the simulators list of traffic lights :D

    def generate_traffic_clusters(self):
        self.traffic_clusters = []

        num_clusters = random.randint(int(self.num_lights*0.65), int(self.num_lights*0.8))
        
        #Choose random traffic lights to associate clusters with
        selected_lights = random.sample(self.traffic_lights, num_clusters)

        for i, light in enumerate(selected_lights):
            #Centers the cluster near this light, slightly before it
            cluster_center = light.position_miles - random.uniform(0.05, 0.1) #cluster is right before light
            cluster_length = random.uniform(0.071, 0.118)  # total length in miles
            padding = cluster_length / 2

            start = max(0, cluster_center - padding) #I found that these numbers give me about 20-30 cars per traffic cluster, which is realistic
            end = min(self.total_distance, cluster_center + padding)
            slowdown_speed = random.uniform(15, 25)  # mph
            deceleration_rate = 3.0  # m/s² — same as acceleration rate I used

            cluster = TrafficCluster(cluster_id=f"cluster_{i+1}", start_position_miles=start, end_position_miles=end, slowdown_speed=slowdown_speed, deceleration_rate=deceleration_rate)
            self.traffic_clusters.append(cluster)


    def run_driver(self, driver): 
        for light in self.traffic_lights:

            for cluster in self.traffic_clusters:

                #Applys cluster if any part of it is between driver's current position and the traffic light
                if driver.position_miles < cluster.end_position_miles and cluster.start_position_miles < light.position_miles: 
                    cluster.apply_cluster_effect(driver)
                    

            driver.travel_to_position(light.position_miles)
            state = light.get_light_state(driver.time_elapsed_sec)
            if(state=="red" or state=="yellow"):
                wait_time = time_until_green(light, driver.time_elapsed_sec)
                driver.wait_at_light(wait_time)
                driver.wait_at_light(driver.get_acceleration_penalty_per_stop())
                driver.red_light_count += 1
    
    def run_simulation(self):
        self.generate_traffic_lights()
        self.generate_traffic_clusters()

        self.steady_driver.reset()
        self.speeder_driver.reset()
        
        self.run_driver(self.steady_driver)
        self.run_driver(self.speeder_driver)

        total_steady_red_lights = self.steady_driver.red_light_count
        total_speeder_red_lights = self.speeder_driver.red_light_count

        steady_driver_final_time = self.steady_driver.time_elapsed_sec
        speeder_final_time = self.speeder_driver.time_elapsed_sec
        time_difference_between_drivers = steady_driver_final_time - speeder_final_time

        print(f"Steady Driver Time: {self.steady_driver.time_elapsed_sec:.2f} seconds")
        print(f"Speeder Driver Time: {self.speeder_driver.time_elapsed_sec:.2f} seconds")
        print(f"Time Difference: {time_difference_between_drivers:.2f} seconds")

        return time_difference_between_drivers, total_steady_red_lights, total_speeder_red_lights
    