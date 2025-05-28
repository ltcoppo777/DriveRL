from models.driver import Driver
from models.traffic_light import TrafficLight
from simulation.simulator import Simulator


def compute_max_possible_saved(dist_miles, steady_speed, speeder_speed): #Helper to calculate max speeder optimal time
    steady_time = (dist_miles / steady_speed) * 3600
    speeder_time = (dist_miles / speeder_speed) * 3600
    return steady_time - speeder_time

if __name__ == "__main__":
    #User Inputs
    total_distance = 10
    num_lights= 16
    speed_limit = 40
    steady_style = "safe"
    speeder_style = "aggressive"

    total_time_differences = 0
    total_steady_reds = 0
    total_speedy_reds = 0

    actual_speeder_speeds = [] #tracks speeds

    for _ in range(1000):
        #Passes driver styles into simulator
        sim = Simulator(total_distance=total_distance, num_lights=num_lights, speed_limit=speed_limit, steady_style=steady_style, speeder_style=speeder_style)
        #Override area: Overrides driver styles directly if needed
        #sim.steady_driver = Driver("d1", speed_limit, driver_style=steady_style)
        #sim.speeder_driver = Driver("d2", speed_limit, driver_style=speeder_style)

        actual_speeder_speeds.append(sim.speeder_driver.speed_mph)

        time_diff, steady_reds, speedy_reds = sim.run_simulation()
        total_time_differences += time_diff
        total_steady_reds += steady_reds
        total_speedy_reds += speedy_reds

    #Averages
    avg_diff = total_time_differences / 1000
    avg_steady_reds = total_steady_reds / 1000
    avg_speedy_reds = total_speedy_reds / 1000

    #Compute % of max saved
    steady_speed = speed_limit  
    avg_speeder_speed = sum(actual_speeder_speeds) / len(actual_speeder_speeds) #average
    max_possible = compute_max_possible_saved(total_distance, steady_speed, avg_speeder_speed)
    percent_saved = (avg_diff / max_possible) * 100 if max_possible else 0

    #Output
    print(f"Distance: {total_distance} miles at {speed_limit} mph")
    print(f"Driver Styles: {steady_style} vs {speeder_style}")
    print(f"Actual Average Speeder Speed: {avg_speeder_speed:.1f} mph")
    print(f"Avg Time Saved: {avg_diff:.2f} sec")
    print(f"Percent of Max Saved: {percent_saved:.2f}%")
    print(f"Avg Steady Reds: {avg_steady_reds:.2f}")
    print(f"Avg Speeder Reds: {avg_speedy_reds:.2f}")