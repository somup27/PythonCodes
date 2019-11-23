# -*- coding: utf-8 -*-
"""Pacman Crash Course

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a3F4UxIraiAJCr4__grOBFTYODVvcrKm
"""

import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Activation, MaxPooling2D, BatchNormalization, Dropout
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from IPython import display

EPISODES = 1000

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        #change these if you would like
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Conv2D(32, kernel_size = 3, activation='relu',input_shape=self.state_size))
        model.add(Conv2D(32, kernel_size = 3, activation = 'relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Conv2D(64,kernel_size = 3, activation = 'relu'))
        model.add(Conv2D(64, kernel_size = 3, activation = 'relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Flatten())
        model.add(Dense(512,activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(self.action_size,activation = 'softmax'))         
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state.reshape(1, *state.shape))
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state.reshape(1, *next_state.shape))[0]))
            target_f = self.model.predict(state.reshape(1, *state.shape))
            target_f[0][action] = target
            self.model.fit(state.reshape(1, *state.shape), target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def show_state(env, step=0, info=""):
    plt.figure(3)
    plt.clf()
    plt.imshow(env.render(mode='rgb_array'))
    plt.title("Step: %d %s" % (step, info))
    plt.axis('off')

    display.clear_output(wait=True)
    display.display(plt.gcf())
    
if __name__ == "__main__":
    env = gym.make('MsPacman-v0')
    state_size = env.observation_space.shape
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    done = False
    batch_size = 32

    for e in range(EPISODES):
        state = env.reset()
        for time in range(500):
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            reward = reward if not done else -10
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print("episode: {}/{}, score: {}, e: {:.2}"
                      .format(e, EPISODES, time, agent.epsilon))
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
                agent.memory= deque([])
        show_state(env,step=e)
        inp = input()