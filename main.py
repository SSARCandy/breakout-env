import cv2
from cv2 import VideoWriter, VideoWriter_fourcc, resize
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


if __name__ == '__main__':
  fourcc = VideoWriter_fourcc(*"XVID")
  vid, size = None, None

  env = Breakout()
  obs = env.reset()
  done = False

  for x in range(2000):
  # while not done:
    action = simple_agent(env)
    img, reward, done, _ = env.step(action)#random.randint(1, 3))
    # print(x, reward, done)
    # cv2.imshow('obs', obs)
    # cv2.waitKey(1)
    # cv2.imwrite('./tmp/{}.png'.format(x), obs)
    if vid is None:
      if size is None:
          size = img.shape[1], img.shape[0]
      vid = VideoWriter('outvid.avi', fourcc, float(30), size, False)
    vid.write(img)
  vid.release()

