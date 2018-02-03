import numpy as np
import matplotlib.pyplot as plt


class Breakout():
  def __init__(self):
    self.shape = (210, 160)
    self.actions = 4
    self.actions_meaning = ['NOOP', 'FIRE', 'RIGHT', 'LEFT']
  
  def step(self, action):
    pass

  def render(self):
    if not self.started:
      return self.obs

    return self.obs

  def reset(self):
    self.score = 0
    self.reward = 0
    self.live = 5
    self.terminal = False
    self.started = False
    self.obs = np.load('start.npy')
    return self.render()


if __name__ == '__main__':
  env = Breakout()
  obs = env.reset()

  plt.imshow(obs, cmap='gray')
  plt.show()
  # obs, _, _, _ = env.step()