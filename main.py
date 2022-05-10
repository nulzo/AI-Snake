import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('abduction2002.ttf', 20)
disp_font = pygame.font.Font('abduction2002.ttf', 14)


#reset
#reward
#play(action)
#game_iteration
#change collision


class Direction(Enum):
    move_right = 1
    move_left = 2
    move_up = 3
    move_down = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
white_color = (255, 255, 255)
fruit_color_outer = (27, 202, 79)
fruit_color_inner = (243,109, 88)
snake_color_outer = (104, 241, 255)
snake_color_inner = (33, 220, 240)
background_color = (0, 0, 0)
black_color = (0, 0, 0)

size_block = 20
speed = 30
high_score = 0


class AISnake:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.high_score = high_score
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Reinforcement Learning Snake')
        self.clock = pygame.time.Clock()
        self.AI_reset()

    def AI_reset(self):
        self.direction = Direction.move_right

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - size_block, self.head.y),
                      Point(self.head.x - (2 * size_block), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame = 0

    def _place_food(self):
        x = random.randint(0, (self.w - size_block) // size_block) * size_block
        y = random.randint(0, (self.h - size_block) // size_block) * size_block
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # move_update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame > 100 * len(self.snake):
            game_over = True
            reward -= 10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. move_update ui and clock
        self._move_update_ui()
        self.clock.tick(speed)
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - size_block or pt.x < 0 or pt.y > self.h - size_block or pt.y < 0:
            if self.score > self.high_score:
                self.high_score = self.score
            return True
        # hits itself
        if self.head in self.snake[1:]:
            if self.score > self.high_score:
                self.high_score = self.score
            return True

        return False

    def _move_update_ui(self):
        self.display.fill(background_color)

        for pt in self.snake:
            pygame.draw.rect(self.display, snake_color_outer, pygame.Rect(pt.x, pt.y, size_block, size_block))
            pygame.draw.rect(self.display, snake_color_inner, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, fruit_color_outer, pygame.Rect(self.food.x, self.food.y, size_block, size_block))
        pygame.draw.rect(self.display, fruit_color_inner, pygame.Rect(self.food.x + 4, self.food.y + 4, 12, 12))

        text = font.render("Score: " + str(self.score), True, white_color)
        high_score = font.render("High Score: " + str(self.high_score), True, white_color)
        if self.high_score <= 10:
            disp = disp_font.render("Nothing but a dumb worm...", True, white_color)
            self.display.blit(disp, [175, 0])
        elif self.high_score > 10:
            disp = disp_font.render("A worm still, but a smarter one...", True, white_color)
            self.display.blit(disp, [200, 0])

        self.display.blit(text, [0, 0])
        self.display.blit(high_score, [450, 0])
        pygame.display.flip()

    def _move(self, action):
        #straigh, move_left, move_right
        order = [Direction.move_right, Direction.move_down, Direction.move_left, Direction.move_up]
        index_of_order = order.index(self.direction)

        if np.array_equal(action,[1,0,0]):
            direct = order[index_of_order]
        elif np.array_equal(action,[0,1,0]):
            new_index = (index_of_order + 1) % 4
            direct = order[new_index]
        else:
            new_index = (index_of_order - 1) % 4
            direct = order[index_of_order]
        self.direction = direct
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.move_right:
            x += size_block
        elif self.direction == Direction.move_left:
            x -= size_block
        elif self.direction == Direction.move_down:
            y += size_block
        elif self.direction == Direction.move_up:
            y -= size_block

        self.head = Point(x, y)
