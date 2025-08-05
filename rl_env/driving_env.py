import gymnasium as gym
from gymnasium import spaces
from simulation.simulator import Simulator 
import numpy as np
from utils.traffic_utils import time_until_green



class DrivingEnv(gym.Env):
    def __init__(self):
        super(DrivingEnv, self).__init__()

        #Defines a simple discrete action space (slow down, maintain, speed up)
        self.action_space = spaces.Discrete(3)

        #Defines an observation space with 3 elements:
        #[distance_to_light, light_color, current_speed]
        low = np.array([0.0, 0.0, 0.0], dtype=np.float32) #using np(numpy) for optimization, easier on the memory since float64 takes twice as much 
        high = np.array([60.0, 2.0, 100.0], dtype=np.float32)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed) #parent reset seed
        self.sim=Simulator( #Creates my new simulator environment
            total_distance=10.0,
            num_lights=16,
            speed_limit=40
        )

        self.sim.generate_traffic_lights() #Runs similar to my main, these lines will essentially create the simulation
        self.sim.generate_traffic_clusters()

        self.driver = self.sim.steady_driver #Training the steady driver in this case

        #all states numbers reset every run
        self.driver.position_miles = 0.0
        self.driver.speed_mph = self.driver.speed_limit_mph  #start at limit
        self.driver.time_elapsed_sec = 0.0
        self.driver.red_light_count = 0
        return self._get_state(), {}

    def _get_state(self):
        next_light = self._get_next_traffic_light_helper()
        
        # Check if there are no more lights ahead
        if next_light is None:
            # Return a terminal state with distance=0, light_color=0 (green), current speed
            return np.array([0.0, 0.0, self.driver.speed_mph], dtype=np.float32)
        
        distance_to_light = next_light.position_miles - self.driver.position_miles
        light_color = self._light_color_index_helper(next_light)
        speed = self.driver.speed_mph

        return np.array([distance_to_light, light_color, speed], dtype=np.float32)
    
    
    def _light_color_index_helper(self, light):
        light_state = light.get_light_state(self.driver.time_elapsed_sec) #using the traff_light class's get_light_state method I made here

        if light_state == "green":
            return 0
        elif light_state == "yellow":
            return 1
        elif light_state == "red":
            return 2
        

    def step(self, action):
        previous_position = self.driver.position_miles

        reward = 0.0
        time_before = self.driver.time_elapsed_sec

        SPEED_STEP = 5 #Driver speeds up or slows down this much based on decisions

        if action == 0: #Slow down
            self.driver.speed_mph = max(0, self.driver.speed_mph - SPEED_STEP)
        elif action == 1: #Maintain speed
            pass
        elif action == 2: #Speed up
            self.driver.speed_mph = min(self.driver.speed_mph + SPEED_STEP, self.driver.speed_limit_mph)

        next_light = self._get_next_traffic_light_helper() #Uses the helper to loop through the lights and see if the driver is behind another light

        if next_light is None:
            reward = 0
            info = {}
            terminated = True
            truncated = False
            return self._get_state(), reward, terminated, truncated, info
        
        for cluster in self.sim.traffic_clusters: #Loops through the clusters in the env and checks if driver is in one
            if(self.driver.position_miles < cluster.end_position_miles and cluster.start_position_miles < next_light.position_miles):
                cluster.apply_cluster_effect(self.driver)

        self.driver.travel_to_position(next_light.position_miles) #Moves the driver

        time_after = self.driver.time_elapsed_sec

        #progress reward for just moving
        progress = (self.driver.position_miles - previous_position) * 100
        reward+=progress

        #time penalty
        reward += -(time_after - time_before)*0.1

        light_state = next_light.get_light_state(self.driver.time_elapsed_sec)
        
        if light_state == "red" or light_state == "yellow":
            wait_time = time_until_green(next_light, self.driver.time_elapsed_sec) #Calculates wait time
            reward -= 2 #Penalty for having to stop
            self.driver.wait_at_light(wait_time) #Waits for red/yellow to turn green
            self.driver.wait_at_light(self.driver.get_acceleration_penalty_per_stop())#Adds penalty for full stop
            self.driver.red_light_count += 1
        else:
            reward+=10 #Bonus for not hitting a red
        
        if self.driver.speed_mph < self.driver.speed_limit_mph - 5:
            reward-=2 #Minor penalty for the driver driving too slow for no reason
        
        terminated = self.driver.position_miles >= self.sim.total_distance
        info = {}

        return self._get_state(), reward, terminated, False, info



    def _get_next_traffic_light_helper(self):
        for light in self.sim.traffic_lights: #Runs loop to check if light is ahead of driver
            if light.position_miles > self.driver.position_miles: 
                return light
        return None #After loop, returns None with no light ahead


    def render(self):
            print(f"Pos: {self.driver.position_miles:.2f} mi | Speed: {self.driver.speed_mph} mph | Time: {self.driver.time_elapsed_sec:.2f} s")
