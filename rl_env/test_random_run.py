import sys
import os
import time

# Add the root directory to the system path so modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Since you're running from OOPSpeedingSimulation directory, use relative import
from rl_env.driving_env import DrivingEnv

def test_random_agent():
    """Test the environment with a random agent"""
    # Instantiate the environment
    env = DrivingEnv()
    obs, _ = env.reset()

    done = False
    total_reward = 0
    step = 0

    print("Starting random driving test...\n")
    print(f"Initial state: {obs}")
    print("Actions: 0=slow down, 1=maintain, 2=speed up\n")

    while not done:
        action = env.action_space.sample()  # Random action
        
        # Use 4 return values instead of 5
        obs, reward, done, info = env.step(action)
        
        print(f"Step {step+1}: Action={action}, Reward={reward:.2f}")
        env.render()  # Print state info
        print(f"Observation: {obs}")
        print("-" * 40)
        
        total_reward += reward
        step += 1
        time.sleep(0.1)  # Slow down so you can read output

    print("\nTest finished.")
    print(f"Total reward: {total_reward:.2f}")
    print(f"Total steps: {step}")
    print(f"Final position: {env.driver.position_miles:.2f} miles")
    print(f"Red lights encountered: {env.driver.red_light_count}")

if __name__ == "__main__":
    test_random_agent()