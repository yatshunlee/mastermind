import numpy as np
from game_env import MastermindEnv

if __name__ == "__main__":
    env = MastermindEnv(display=True)
    observation = env.reset()

    while True:
        action = input('Guess from 1 - 6 with format _, _, _, _:')
        if action == 'q':
            break
        action = list(map(int, action.split(',')))
        action = np.array(action)
        observation, reward, done, info = env.step(action)
        print(observation)
        if done:
            observation = env.reset()