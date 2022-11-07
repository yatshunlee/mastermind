import numpy as np
from game_env import MastermindEnv

if __name__ == "__main__":
    env = MastermindEnv(display=True)
    observation = env.reset()

    while True:
        while True:
            action = input('Guess from 1 - 6 with format _, _, _, _ (or input q to quit):')
            if action == 'q':
                exit(0)
            try:
                action = list(map(int, action.split(',')))
                if len(action) == 4:
                    action = np.array(action)
                    break
            except:
                pass
                
        observation, reward, done, info = env.step(action)
        print('\n# 1  2  3  4  R  W #\n')
        print(observation)
        if done:
            observation = env.reset()