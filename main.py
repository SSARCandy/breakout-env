import numpy as np
import random
import matplotlib.pyplot as plt


class BreakoutPlayer():
  def __init__(self):
    pass
  
  def render(self):
    pass

# class Ball():
  # def __init__(self, pos, v):
    # self.pos = pos
    # self.v = v
  # def step

class GameObject():
  def __init__(self, pos, size):
    self.pos = pos
    self.size = size

  def translate(self, translate):
    self.pos[0] += translate[0]
    self.pos[1] += translate[1]

  def boundingbox(self):
    # BB = (y1, y2, x1, x2)
    return [self.pos[0], self.pos[0] + self.size[0], self.pos[1], self.pos[1] + self.size[1]]
    

# class Bricks():
#   def __init__(self, rows, cols, brick_size):
#     self.bricks_pos = [57, 8]
#     self.rows = rows
#     self.cols = cols
#     self.brick_size = brick_size
#     self.bricks = []

#     for r in range(self.rows):
#       y = self.bricks_pos[0] + r*self.brick_size[0]
#       x = self.bricks_pos[1]
#       row_bricks = self.__create_rows([y, x])
      
#   def __create_rows(self, pos):
#     rows = [GameObject([pos[0], pos[1] + p*self.brick_size[1]], self.brick_size) for p in range(self.cols)]
#     return rows


class Breakout():
  def __init__(self):
    self.shape = (210, 160)
    self.actions = 4
    self.actions_meaning = ['NOOP', 'FIRE', 'RIGHT', 'LEFT']
  
  def step(self, action):
    if not 0 < action < self.actions:
      raise IndexError

    act = self.actions_meaning[action]

    if act == 'RIGHT':
      self.paddle.translate(self.paddle_v)
    if act == 'LEFT':
      self.paddle.translate([-x for x in self.paddle_v])

    if self.started:
      self.ball.translate(self.ball_v)
      
      # Check collision
      # Frame BB
      # Paddle BB
      # Bricks BB

    # Check is FIRE
    if self.actions_meaning[action] == 'FIRE':
      self.started = True
    
    # (obs, reward, done, info)
    return self.render(), 0, self.terminal, None

  def render(self):
    obs = np.copy(self.obs_base)

    # Draw paddle
    paddle_bb = self.paddle.boundingbox()
    obs[paddle_bb[0]:paddle_bb[1], paddle_bb[2]:paddle_bb[3]] = 143

    if not self.started:
      return obs

    # Draw ball
    ball_bb = self.ball.boundingbox()
    obs[ball_bb[0]:ball_bb[1], ball_bb[2]:ball_bb[3]] = 143

    # Draw bricks

    # Draw info (score, live)

    return obs

  def reset(self):
    self.score = 0
    self.reward = 0
    self.live = 5
    self.terminal = False
    self.started = False
    self.obs_base = np.load('base.npy')
    self.ball = GameObject([100, 100], [5, 2])
    self.ball_v = [2, -1]
    self.paddle = GameObject([189, 99], [4, 15])
    self.paddle_v = [0, 2]
    # self.bricks = 
    return self.render()


if __name__ == '__main__':
  env = Breakout()
  obs = env.reset()

  plt.ion()
  plt.show()
  for _ in range(20):
    obs, _, _, _ = env.step(random.randint(1, 3))
    plt.imshow(obs, cmap='gray')
    plt.pause(.05)