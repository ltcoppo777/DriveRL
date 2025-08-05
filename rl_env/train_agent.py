from stable_baselines3 import PPO
from rl_env.driving_env import DrivingEnv

env = DrivingEnv() #creates my environment


#I initialize the PPO with MLP policy
model = PPO(
    policy="MlpPolicy",
    env=env,
    verbose=1
)

print("✅ PPO model initialized successfully!")

#Trains the agent (model) for 10,000 timesteps (reminder for me: will increase in a bit)
model.learn(total_timesteps=900000)

#Save the trained model so I dont have to redo all of the steps, and I can just resume
model.save("ppo_driver_env_v2")

print("✅ Model trained and saved as ppo_driver_env_v2.zip") #The other ppo_driver zip is an initial test, so I kept it for history!

