import gym
import nle
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
env = make_vec_env("NetHackScore-v0")
model = PPO('MlpPolicy', env, learning_rate=1e-3, verbose=1)
model.learn(total_timesteps=25000)
model.save('ppo-nethack')






# mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, done,  info = env.step(action)
    env.render()
