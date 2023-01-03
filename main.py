import argparse
import numpy as np
from time import sleep
from game_env import MastermindEnv
from stable_baselines3 import A2C, PPO

def play_game():
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
        if not done:
            print('\n# 1  2  3  4  R  W #\n')
            print(observation)
        else:
            observation = env.reset()

def train(total_timesteps=100000, name='MODEL'):
    env = MastermindEnv()

    model = A2C("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=total_timesteps)
    model.save(name)
    
    print('The trained model is saved as MODEL.zip')

def test(model, name='MODEL'):
    model = A2C.load(model)

    env = MastermindEnv(display=True)
    observation = env.reset()

    while True:
        action, _ = model.predict(observation, deterministic=True)
        observation, reward, done, info = env.step(action)
        sleep(0.2)
        if not done:
            print('\n# 1  2  3  4  R  W #\n')
            print(observation)
        else:
            observation = env.reset()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--play', action='store_true', help='play game')
    parser.add_argument('--train', action='store_true', help='train')
    parser.add_argument('--test', action='store_true', help='test')
    parser.add_argument('--model', help='incl. the trained model for testing')

    args = parser.parse_args()

    if args.play:
        play_game()
    elif args.train:
        train()
    elif args.test:
        model = args.model
        if model:
            test(model)
        else:
            print('Usage: python main.py --test [--model MODEL].')
    else:
        print('Usage: python main.py [--play] [--train] [--test] [--model MODEL]')