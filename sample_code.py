import random
import itertools
from breakout_env import Breakout
from cv2 import VideoWriter, VideoWriter_fourcc, imshow, waitKey

def simple_agent(env):
  if not env.started:
    return 1

  ball_pos = env.ball.center()
  paddle_pos = env.paddle.center()

  if paddle_pos[1] < ball_pos[1]:
    return 2
  else:
    return 3


vid = VideoWriter('demo.avi', VideoWriter_fourcc(*"XVID"), float(30), (160, 210), False)

env = Breakout({
    'max_step': 1000,
    'lifes': 7,
    'ball_speed': [-5, -2],
    'ball_size': [5, 2],
    'paddle_width': 30,
    'paddle_speed': 5
  })
  
for ep in range(1):
  obs = env.reset()
  for t in itertools.count():
    action = random.randint(0, env.actions - 1)
    obs, reward, done, _ = env.step(2)
    print('Epsoide: {}, Step: {}, Reward: {}, Done: {}'.format(ep, t, reward, done))
    imshow('obs', obs)
    waitKey(1)
    vid.write(obs)
    if done:
      break

vid.release()
