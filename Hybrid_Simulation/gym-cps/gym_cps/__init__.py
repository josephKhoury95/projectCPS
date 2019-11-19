from gym.envs.registration import register

register(
    id='cps-v0',
    entry_point='gym_cps.envs:CpsEnv',
)
