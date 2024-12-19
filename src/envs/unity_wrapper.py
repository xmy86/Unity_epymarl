import gymnasium as gym
from gymnasium.spaces import Tuple, Box

import numpy

from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.envs.unity_parallel_env import UnityParallelEnv


class UnityWrapper(gym.Env):
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 5,
    }

    def __init__(self, seed=None, **kwargs):
        self.unity_env = UnityEnvironment(file_name=kwargs['unity_env_path'], 
                                     no_graphics=not kwargs['graphics'], 
                                     seed=kwargs['seed'] if seed is None else seed)
        self._env = UnityParallelEnv(self.unity_env)
        
        self.n_agents = self._env.num_agents
        self.last_obs = self._env.reset()

        self.action_space = Tuple(
            tuple([Box(low=self._env.action_spaces[k].low, 
                       high=self._env.action_spaces[k].high, 
                       shape=self._env.action_spaces[k].shape, 
                       dtype=self._env.action_spaces[k].dtype) for k in self._env.agents])
        )

        self.observation_space = Tuple(
            tuple([Box(low=self._env.observation_spaces[k].low, 
                       high=self._env.observation_spaces[k].high, 
                       shape=self._env.observation_spaces[k].shape, 
                       dtype=self._env.observation_spaces[k].dtype) for k in self._env.agents])
        )

    def reset(self, *args, **kwargs):
        obs = self._env.reset()
        obs = tuple([obs[k] for k in self._env.agents])
        self.last_obs = obs
        return obs

    def render(self):
        return self._env.render()

    def step(self, actions):
        dict_actions = {}
        for agent, action in zip(self._env.agents, actions):
            dict_actions[agent] = numpy.clip(action*5, -1, 1)

        observations, rewards, _, truncated = self._env.step(dict_actions)

        obs = tuple([observations[k] for k in self._env.agents])
        rewards = [rewards[k] for k in self._env.agents]
        done = all([False for _ in self._env.agents]) #
        truncated = all([False for _ in self._env.agents]) #
        if done:
            # empty obs and rewards for PZ environments on terminated episode
            assert len(obs) == 0
            assert len(rewards) == 0
            obs = self.last_obs
            rewards = [0] * len(obs)
        else:
            self.last_obs = obs
        return obs, rewards, done, truncated

    def close(self):
        return self._env.close()


# import Unity environment
gym.register(
    id="unity_env",
    entry_point="envs.unity_wrapper:UnityWrapper",
    kwargs={
        "unity_env_path": "Combat_win/UnityEnvironment.exe",
        "graphics": True,
        "seed": 42
    }
)