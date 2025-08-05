import gymnasium as gym
from stable_baselines3 import PPO
from rl_env.driving_env import DrivingEnv
from simulation.simulator import Simulator

model = PPO.load(r"C:\Users\lukec\OneDrive\Desktop\OOPSpeedingSimulation\SpeedingSimulationBackend\ppo_driver_env_v2")
env = DrivingEnv() #same environment as training

episodes = 10 #number of episodes ran for testing
total_rewards = []
red_light_counts = []
final_times = []


#AI DRIVER

print("=== Evaluating Trained AI Agent ===\n")


for ep in range(episodes):
    obs, _ = env.reset()
    done = False
    episode_reward = 0
    
    while not done:
        # Let AI model predict action based on current state
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        episode_reward += reward
    
    total_rewards.append(episode_reward)
    red_light_counts.append(env.driver.red_light_count)
    final_times.append(env.driver.time_elapsed_sec)
    
    print(f"Episode {ep+1}: Reward={episode_reward:.2f}, "
          f"Red Lights={env.driver.red_light_count}, "
          f"Final Time={env.driver.time_elapsed_sec:.2f} sec")

# Average performance
print("\n=== AI Agent Results ===")
print(f"Average Reward: {sum(total_rewards)/episodes:.2f}")
print(f"Average Red Lights: {sum(red_light_counts)/episodes:.2f}")
print(f"Average Final Time: {sum(final_times)/episodes:.2f} sec")



#REGULAR NON AI DRIVER

baseline_times = []
baseline_reds = []

print("\n=== Evaluating Baseline Regular Driver ===\n")

for ep in range(episodes):
    sim = Simulator(total_distance=10.0, num_lights=16, speed_limit=40)
    sim.generate_traffic_lights()
    sim.generate_traffic_clusters()
    
    # Use the "steady" driver (not the aggressive one)
    sim.run_driver(sim.steady_driver)
    
    baseline_times.append(sim.steady_driver.time_elapsed_sec)
    baseline_reds.append(sim.steady_driver.red_light_count)
    
    print(f"Episode {ep+1}: Red Lights={sim.steady_driver.red_light_count}, "
          f"Final Time={sim.steady_driver.time_elapsed_sec:.2f} sec")

print("\n=== Baseline Driver Results ===")
print(f"Average Red Lights: {sum(baseline_reds)/episodes:.2f}")
print(f"Average Final Time: {sum(baseline_times)/episodes:.2f} sec")



#SPEEDER NON AI DRIVER

print("\n=== Evaluating Baseline Speeder Driver ===")

total_red_speeder = 0
total_time_speeder = 0

for ep in range(10):
    sim = Simulator(total_distance=10.0, num_lights=16, speed_limit=40)
    sim.generate_traffic_lights()
    sim.generate_traffic_clusters()

    speeder = sim.speeder_driver
    speeder.reset()

    sim.run_driver(speeder)

    total_red_speeder += speeder.red_light_count
    total_time_speeder += speeder.time_elapsed_sec

    print(f"Episode {ep+1}: Red Lights={speeder.red_light_count}, Final Time={speeder.time_elapsed_sec:.2f} sec")

avg_red_speeder = total_red_speeder / 10
avg_time_speeder = total_time_speeder / 10

print("\n=== Speeder Driver Results ===")
print(f"Average Red Lights: {avg_red_speeder:.2f}")
print(f"Average Final Time: {avg_time_speeder:.2f} sec")






print("\n=== Final Comparison ===")
ai_avg_time = sum(final_times) / episodes
ai_avg_reds = sum(red_light_counts) / episodes
steady_avg_time = sum(baseline_times) / episodes
steady_avg_reds = sum(baseline_reds) / episodes

print(f"AI Driver     -> Time: {ai_avg_time:.2f}s | Red Lights: {ai_avg_reds:.2f}")
print(f"Steady Driver -> Time: {steady_avg_time:.2f}s | Red Lights: {steady_avg_reds:.2f}")
print(f"Speeder Driver-> Time: {avg_time_speeder:.2f}s | Red Lights: {avg_red_speeder:.2f}")
