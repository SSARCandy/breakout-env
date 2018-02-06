import numpy as np
import random
import matplotlib.pyplot as plt
import cv2

FRAME_X = [7, 152]
FRAME_Y = [31, 194]

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
  def __init__(self, pos, size, color=143, reward=0):
    self.pos = pos
    self.size = size
    self.color = color
    self.reward = reward

  def translate(self, translate):
    self.pos[0] += translate[0]
    self.pos[1] += translate[1]

  def boundingbox(self):
    # BB = (y1, y2, x1, x2)
    return [self.pos[0], self.pos[0] + self.size[0], self.pos[1], self.pos[1] + self.size[1]]
    

class Bricks():
  def __init__(self, rows, cols, brick_size):
    self.bricks_pos = [57, 8]
    self.rows = rows
    self.cols = cols
    self.brick_size = brick_size
    self.bricks = []

    for r in range(self.rows):
      y = self.bricks_pos[0] + r*self.brick_size[0]
      x = self.bricks_pos[1]
      row_bricks = self.__create_rows([y, x], 200 - 20*r, self.rows - r)
      self.bricks += row_bricks
      
  def __create_rows(self, pos, c, r):
    rows = [GameObject([pos[0], pos[1] + p*self.brick_size[1]], self.brick_size, c, r) for p in range(self.cols)]
    return rows


def aabb(bb1, bb2):
  if bb1[0] < bb2[0]:
    return bb1[0] < bb2[1] and bb1[1] > bb2[0] and bb1[2] < bb2[3] and bb1[3] > bb2[2]
  else:
    return bb2[0] < bb1[1] and bb2[1] > bb1[0] and bb2[2] < bb1[3] and bb2[3] > bb1[2]
    

class Breakout():
  def __init__(self):
    self.shape = (210, 160)
    self.actions = 4
    self.actions_meaning = ['NOOP', 'FIRE', 'RIGHT', 'LEFT']
    self.obs_base = np.load('./asserts/base.npy')
    self.digits = [np.load('./asserts/{}.npy'.format(i)) for i in range(10)]
    self.render_bb = {
      'scores': [[5, 15, 36, 48], [5, 15, 52, 64], [5, 15, 68, 80]],
      'live': [5, 15, 100, 112],
      'level': [5, 15, 128, 140]
    }
  
  def step(self, action):
    if self.terminal:
      raise RuntimeError('Take action after game terminated.')
    if not 0 < action < self.actions:
      raise IndexError('Selected action out of range.')

    act = self.actions_meaning[action]

    if act == 'RIGHT':
      self.paddle.translate(self.paddle_v)
    if act == 'LEFT':
      self.paddle.translate([-x for x in self.paddle_v])

    if self.started:
      self.ball.translate(self.ball_v)
      
      # Check collision
      self.__edge_collision()
      self.__paddle_collision()
      self.reward = self.__bricks_collision()
      self.score += self.reward

    # Check is FIRE
    if self.actions_meaning[action] == 'FIRE':
      self.started = True
    
    # (obs, reward, done, info)
    return self.render(), self.reward, self.terminal, None

  def render(self):
    obs = np.copy(self.obs_base)

    # Draw paddle
    paddle_bb = self.paddle.boundingbox()
    obs[paddle_bb[0]:paddle_bb[1], paddle_bb[2]:paddle_bb[3]] = self.paddle.color

    # Draw bricks
    for brick in self.bricks.bricks:
      bb = brick.boundingbox()
      obs[bb[0]:bb[1], bb[2]:bb[3]] = brick.color

    # Draw ball
    if self.started:
      ball_bb = self.ball.boundingbox()
      obs[ball_bb[0]:ball_bb[1], ball_bb[2]:ball_bb[3]] = self.ball.color

    # Draw info (score, live)
    live_bb = self.render_bb['live']
    obs[live_bb[0]:live_bb[1], live_bb[2]:live_bb[3]] = self.digits[self.live]

    scores_bb = self.render_bb['scores']
    scores = [self.score // 10**i for i in range(2, -1, -1)]
    for idx, bb in enumerate(scores_bb, 0):
      obs[bb[0]:bb[1], bb[2]:bb[3]] = self.digits[scores[idx]]

    return obs

  def reset(self):
    self.score = 0
    self.reward = 0
    self.live = 5
    self.terminal = False
    self.started = False
    self.ball = GameObject([100, 10], [5, 2])
    self.ball_v = [-5, -2]
    self.paddle = GameObject([189, 9], [4, 15])
    self.paddle_v = [0, 2]
    self.bricks = Bricks(6, 18, [6, 8])
    return self.render()

  def __edge_collision(self):
    bb1 = self.ball.boundingbox()
    if aabb(bb1, [0, 999, 0, FRAME_X[0]]): # Left edge
      self.ball_v = [self.ball_v[0], -self.ball_v[1]]
      self.ball.translate([0, 2*self.ball_v[1]])
    elif aabb(bb1, [0, 999, FRAME_X[1], 999]): # Right edge
      self.ball_v = [self.ball_v[0], -self.ball_v[1]]
      self.ball.translate([0, 2*self.ball_v[1]])
    elif aabb(bb1, [0, FRAME_Y[0], 0, 999]): # Top edge
      self.ball_v = [-self.ball_v[0], self.ball_v[1]]
      self.ball.translate([2*self.ball_v[0], 0])
    elif aabb(bb1, [FRAME_Y[1], 999, 0, 999]): # Bottom edge
      self.live -= 1
      self.terminal = self.started and self.live == 0
      self.ball = GameObject([100, 10], [5, 2])
      self.ball_v = [-2, -2]

  def __paddle_collision(self):
    bb1 = self.ball.boundingbox()
    if aabb(bb1, self.paddle.boundingbox()):
      self.ball_v = [-self.ball_v[0], self.ball_v[1]]
      self.ball.translate([2*self.ball_v[0], 0])

  def __bricks_collision(self):
    bb1 = self.ball.boundingbox()
    x2 = (bb1[2] + bb1[3]) / 2.0
    # y2 = (bb1[0] + bb1[1]) / 2.0
    x1 = x2 - self.ball_v[1]
    # y1 = y2 - self.ball_v[0]

    for idx, brick in enumerate(self.bricks.bricks):
      bb2 = brick.boundingbox()

      if not aabb(bb1, bb2):
        continue

      if (x1 < bb2[2] and x2 > bb2[2]) or (x1 > bb2[3] and x2 < bb2[3]):
        self.ball_v = [self.ball_v[0], -self.ball_v[1]]
        self.ball.translate([0, 2*self.ball_v[1]])
      else:
        self.ball_v = [-self.ball_v[0], self.ball_v[1]]
        self.ball.translate([2*self.ball_v[0], 0])

      r = brick.reward
      del self.bricks.bricks[idx]
      return r

    return 0


if __name__ == '__main__':
  env = Breakout()
  obs = env.reset()

  # plt.ion()
  # plt.show()
  for x in range(5000):
    obs, reward, done, _ = env.step(1)#random.randint(1, 3))
    print(x, reward, done)
    cv2.imshow('tt', obs)
    cv2.waitKey(1)
    # plt.imshow(obs, cmap='gray')
    # plt.pause(0.01)