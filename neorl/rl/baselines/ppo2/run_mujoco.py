#!/usr/bin/env python3
import numpy as np
import gym

from neorl.rl.baselines.shared.cmd_util import mujoco_arg_parser
from neorl.rl.baselines.shared import logger
from neorl.rl.baselines.shared.monitor import Monitor
from neorl.rl.baselines.shared import set_global_seeds
from neorl.rl.baselines.shared.vec_env.vec_normalize import VecNormalize
from neorl.rl.baselines.ppo2.ppo2 import PPO2
from neorl.rl.baselines.shared.policies import MlpPolicy
from neorl.rl.baselines.shared.vec_env.dummy_vec_env import DummyVecEnv


def train(env_id, num_timesteps, seed):
    """
    Train PPO2 model for Mujoco environment, for testing purposes

    :param env_id: (str) the environment id string
    :param num_timesteps: (int) the number of timesteps to run
    :param seed: (int) Used to seed the random generator.
    """
    def make_env():
        env_out = gym.make(env_id)
        env_out = Monitor(env_out, logger.get_dir(), allow_early_resets=True)
        return env_out

    env = DummyVecEnv([make_env])
    env = VecNormalize(env)

    set_global_seeds(seed)
    policy = MlpPolicy
    model = PPO2(policy=policy, env=env, n_steps=2048, nminibatches=32, lam=0.95, gamma=0.99, noptepochs=10,
                 ent_coef=0.0, learning_rate=3e-4, cliprange=0.2)
    model.learn(total_timesteps=num_timesteps)

    return model, env


def main():
    """
    Runs the test
    """
    args = mujoco_arg_parser().parse_args()
    logger.configure()
    model, env = train(args.env, num_timesteps=args.num_timesteps, seed=args.seed)

    if args.play:
        logger.log("Running trained model")
        obs = np.zeros((env.num_envs,) + env.observation_space.shape)
        obs[:] = env.reset()
        while True:
            actions = model.step(obs)[0]
            obs[:] = env.step(actions)[0]
            env.render()


if __name__ == '__main__':
    main()
