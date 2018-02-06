from cv2 import VideoWriter, VideoWriter_fourcc, resize, imshow, waitKey
from breakout_env import Breakout

def simple_agent(env):
  if not env.started:
    return 1

  ball_xs = env.ball.boundingbox()
  paddle_xs = env.paddle.boundingbox()

  ball_x = ball_xs[2]+ball_xs[3]/2.0
  paddle_x = paddle_xs[2]+paddle_xs[3]/2.0

  if paddle_x < ball_x:
    return 2
  else:
    return 3


vid = VideoWriter('demo.avi', VideoWriter_fourcc(*"XVID"), float(30), (160, 210), False)

env = Breakout()
obs = env.reset()
done = False

# while not done:
for x in range(2000):
  action = simple_agent(env)
  img, reward, done, _ = env.step(action)
  # print(x, reward, done)
  imshow('obs', obs)
  waitKey(1)
  vid.write(img)
vid.release()

