import numpy as np
from time import sleep
from gym import Env, spaces

class MastermindEnv(Env):
    def __init__(self, display=False, num_actions=4, num_turns=8, num_obs=7):
        """
        :param: render_rule: to show rule when playing manually
        :built-in parameters: self.observation_space:
        :built-in parameters: self.action_space:
        :built-in parameters: self.game_rule:
        :built-in parameters: self.render_rule:
        """
        # super(MastermindEnv).__init()
        self.observation_space = spaces.Box(low=0, high=6, shape=(1, 7), dtype=np.uint8)
        # self.observation_space = spaces.Box(low=0, high=6, shape=(1, 7), dtype=np.uint8)
        # self.observation_space = spaces.Box(low=0, high=6, shape=(8, 6), dtype=np.uint8)
        self.action_space = spaces.MultiDiscrete([6, 6, 6, 6])
        
        self.guessed = []

        self.num_actions = num_actions
        self.num_turns = num_turns
        self.game_rule = '''
  MASTERMIND

  [OBJECTIVE] You must crack the secret code in the fewest number of guesses.

    Rule#1: There are 8 turns in total. You must guess it correctly within 8 guesses.
    Rule#2: There are in total 6 numbers (1-6). It can be a repeatable pattern of
            4 digits out of the 6 numbers.
    Rule#3: After each guess, the terminal will show how many #red and #white you got:
              - Red: Correct number and position
              - White: Correct number but not in the correct location.
    Rule#4: You modify your answer accordingly after each round and try
            to make a right guess of the code.

    Enjoy! :)
                    '''
        self.display = display

    def reset(self):
        # initialize the true pattern randomly
        self.true = np.random.randint(1, 7, self.num_actions)
        self.num_actions = len(self.true)
        # total number of rounds
        self.num_of_turns = 0
        # board state
        self.board = np.zeros((self.num_turns, self.num_actions))
        # score state
        self.score = np.zeros((self.num_turns, 2))
        # end state
        self.end = np.zeros((self.num_turns, 1))
        # gameover
        self.done = False
        
        self.guessed = []

        # print game rule
        if self.display:
            print(self.game_rule)

        # to make it a box with (8, 6) shape
        states = np.c_[self.board, self.score, self.end]
        
        states = states[self.num_of_turns, :]
        states = states.reshape((1, 7))
        
        return states

    def step(self, action):
        action = np.array(action).reshape(self.num_actions)
        # calculate the score: #red and #white
        rw_scores = self.scoring(action, self.true)
        # update board obs
        self.board[self.num_of_turns, :] = action
        # update score obs
        self.score[self.num_of_turns, :] = rw_scores
        # check terminate
        self.num_of_turns += 1
        # Either guess correctly or time's up
        self.done = self.game_end(rw_scores[0], self.num_of_turns)
        # update end obs
        self.end[self.num_of_turns - 1, :] = 1.0 if self.done else 0.0
        # init reward function (can customize)
        # reward = 1 if rw_scores[0]==self.num_actions else 0
        if tuple(action) in self.guessed:
            reward = 0
        else:
            reward = rw_scores[0]
            self.guessed.append(tuple(action))
        # to make it a box with (8, 6) shape
        states = np.c_[self.board, self.score, self.end]
        
        states = states[self.num_of_turns - 1, :]
        states = states.reshape((1, 7))
        
        return states, reward, self.done, {}

    def render(self):
        if self.done:
            pass
        elif self.game_start:
            pass
        else:
            pass

    def scoring(self, guess, true):
        R, W = 0, 0

        # hashmap: storing the true value w.r.t. its occurance
        true_hash = {}
        for i in range(self.num_actions):
            if true[i] in true_hash:
                true_hash[true[i]] += 1
            else:
                true_hash[true[i]] = 1

        # avoid duplicated guessing
        # e.g. true = [4,3,2,3]; guess = [1,3,0,5]
        # count num red
        guessed = []
        for i in range(self.num_actions):
            if guess[i] == true[i]:
                R += 1
                true_hash[true[i]] -= 1
                guessed.append(i)
        # count num white
        for i in range(self.num_actions):
            if guess[i] in true_hash and true_hash[guess[i]] > 0 and not i in guessed:
                W += 1
                true_hash[guess[i]] -= 1

        return np.array([R, W])

    def game_end(self, red, num_of_turns):
        """
        :params: true: true arragnment
        :params: red: num. of guesses that agent/player guesses correctly
        :params: num_of_turns: count to end the game
        """
        if red == self.num_actions:
            if self.display:
                print('  [END] Congrats!!! You made a correct guess.\n')
                sleep(.5)
            return True

        if num_of_turns == self.num_turns:
            if self.display:
                print(f'  [END] Better luck next time. The correct answer is {self.true}\n')
                sleep(.5)
            return True

        return False