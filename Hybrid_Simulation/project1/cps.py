import gym
import gym_cps

## Make the environment
env = gym.make('cps-v0')

done = False
observation = env.observation
steps = 0
print env.render()

def main_loop():
    while not done:
        steps += 1
        action = env.attacker_action_space_sample(observation)
        observation, reward_a, reward_b, done = env.step(action)

        if done:
            break


print 'I am here!!!'
