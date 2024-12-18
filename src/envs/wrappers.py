from gymnasium import Wrapper, spaces
import numpy as np


class FlattenObservation(Wrapper):
    r"""Observation wrapper that flattens the observation of individual agents."""

    def __init__(self, env):
        super(FlattenObservation, self).__init__(env)

        ma_spaces = []

        for sa_obs in env.observation_space:
            flatdim = spaces.flatdim(sa_obs)
            ma_spaces += [
                spaces.Box(
                    low=-float("inf"),
                    high=float("inf"),
                    shape=(flatdim,),
                    dtype=np.float32,
                )
            ]

        self.observation_space = spaces.Tuple(tuple(ma_spaces))

    def reset(self, seed=None, options=None):
        result = self.env.reset(seed=seed, options=options)
        if not isinstance(result[0], tuple):
            return self._flatten_obs(result)
        obs, info = result
        return self._flatten_obs(obs)

    def step(self, actions):
        obs, rew, done, truncated = self.env.step(actions)
        return self._flatten_obs(obs), rew, done, truncated

    def _flatten_obs(self, observation):
        return tuple(
            [
                spaces.flatten(obs_space, obs)
                for obs_space, obs in zip(self.env.observation_space, observation)
            ]
        )
