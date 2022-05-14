import torch
import random
import numpy as np
from AIClasses import AISnake, Direction, Point
from collections import deque
from AITrainer import *
from Plotter import plotter
"""https://towardsdatascience.com/snake-played-by-a-deep-reinforcement-learning-agent-53f2c4331d36"""
"""https://www.youtube.com/watch?v=PJl4iabBEz0"""
"""Expanded upon concepts in these materials"""

max_mem = 100_000
batch = 1000
learning_rate = 0.001


class Agent:
    def __init__(self):
        self.num_games = 0
        #random controller
        self.epsilon = 0
        #discount rate; Must be smaller than 1
        self.gammma = 0.9
        #pops elements on the left if max memory sice is reached
        self.mem = deque(maxlen=max_mem)
        self.model = Linear_Qnet(11, 256, 3)
        self.trainer = QTrainer(self.model, learning_rate=learning_rate, gamma=self.gammma)

    def get_state(self, game):
        snake_head = game.snake[0]
        left_point = Point(snake_head.x - 20, snake_head.y)
        right_point = Point(snake_head.x + 20, snake_head.y)
        up_point = Point(snake_head.x, snake_head.y - 20)
        down_point = Point(snake_head.x, snake_head.y + 20)

        left_direction = game.direction == Direction.move_left
        right_direction = game.direction == Direction.move_right
        up_direction = game.direction == Direction.move_up
        down_direction = game.direction == Direction.move_down

        state = [
            #Danger ahead
            (left_direction and game.is_collision(left_point)) or
            (right_direction and game.is_collision(right_point)) or
            (up_direction and game.is_collision(up_point)) or
            (down_direction and game.is_collision(down_point)),
            #Danger right
            (left_direction and game.is_collision(up_point)) or
            (right_direction and game.is_collision(down_point)) or
            (up_direction and game.is_collision(right_point)) or
            (down_direction and game.is_collision(left_point)),
            #Danger left
            (left_direction and game.is_collision(down_point)) or
            (right_direction and game.is_collision(up_point)) or
            (up_direction and game.is_collision(left_point)) or
            (down_direction and game.is_collision(right_point)),
            #Move Direction
            left_direction,
            right_direction,
            up_direction,
            down_direction,
            #Treat location
            game.food.x < game.head.x, # treat left
            game.food.x > game.head.x, # Treat right
            game.food.y < game.head.y, #treat up
            game.food.y > game.head.y, #treat down
            ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.mem.append((state, action, reward, next_state, game_over))

    def train_Lmemory(self):
        #training the models long term memory
        if len(self.mem) > batch:
            sample = random.sample(self.mem, batch) # return list of tuples
        else:
            sample = self.mem

        states, actions, rewards, next_states, game_over = zip(*sample) #getting all variables to use for training
        self.trainer.trainer(states, actions, rewards, next_states, game_over)

    def train_Smemory(self, state, action, reward, next_state, game_over):
        self.trainer.trainer(state, action, reward, next_state, game_over)

    def get_action(self, state):
        #exploration and exploitation
        self.epsilon = 80 - self.num_games
        final = [0, 0, 0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0, 2)
            final[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float) #convert to tensor
            predict = self.model(state0) # make prediction
            move = torch.argmax(predict).item() # convert to int
            final[move] = move
        return final


def train():
    scores = []
    mean_scores = []
    total = 0
    highest = 0
    agent = Agent()
    game = AISnake()
    while True:
        #getting current state
        state = agent.get_state(game)
        #get move
        final_move = agent.get_action(state)
        #perfome move
        reward, game_over, score = game.play_step(final_move)
        new_state = agent.get_state(game)
        #train short memory
        agent.train_Smemory(state, final_move, reward, new_state, game_over)
        #remember
        agent.remember(state, final_move, reward, new_state, game_over)
        if game_over:
            #train long memory/replay memory
            #plot results
            game.AI_reset()
            agent.num_games += 1
            agent.train_Lmemory()
            if score > highest:
                highest = score
                #agent.model.save()
            print('Game:', agent.num_games, 'Score:', score, "Record:", highest)
            scores.append(score)
            total += score
            mean_score = total / agent.num_games
            mean_scores.append(mean_score)
            plotter(scores, mean_scores)


if __name__ == "__main__":
    train()


