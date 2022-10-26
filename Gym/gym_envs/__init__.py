from gym.envs.registration import register

register(
    id='gym_envs/GridWorld-v0',
    entry_point='gym_envs.envs:GridWorld',
    max_episode_steps=300,
)