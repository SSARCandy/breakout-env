# Breakout-env

A configurable Breakout environment.

## Configure Options

| Option         | Description                     | Type         | Range      | Default Value |
|----------------|---------------------------------|--------------|------------|---------------|
| `max_step`     | Max step per episode.           | `int`        | 0 ~ Inf    | 10000         |
| `lifes`        | Lifes                           | `int`        | 0 ~ Inf    | 5             |
| `ball_speed`   | Ball's initial velocity. [y, x] | `[int, int]` | -Inf ~ Inf | [-5, 2]       |
| `ball_color`   | Ball's color (gray scale)       | `int`        | 0 ~ 255    | 143           |
| `ball_size`    | Ball's size [h, w]              | `[int, int]` | 1 ~ Inf    | [5, 2]        |
| `paddle_width` | Paddle's width                  | `int`        | 1 ~ 100    | 15            |
| `paddle_color` | Paddle color (gray scale)       | `int`        | 0 ~ 255    | 143           |
| `paddle_speed` | Paddle moving speed             | `int`        | 1 ~ Inf    | 2             |
|                |                                 |              |            |               |
|                |                                 |              |            |               |

## Example

```py
import cv2
import random
import itertools
from breakout_env import Breakout

env = Breakout({
    'max_step': 1000,
    'lifes': 7,
    'ball_speed': [-5, -2],
    'ball_size': [5, 2],
    'paddle_width': 30,
    'paddle_speed': 5
  })

for ep in range(2):
  obs = env.reset()
  for t in itertools.count():
    action = random.randint(0, env.actions - 1)
    obs, reward, done, _ = env.step(action)
    print('Episode: {}, Step: {}, Reward: {}, Done: {}'.format(ep, t, reward, done))
    cv2.imshow('obs', obs)
    cv2.waitKey(1)
    if done:
      break
```


## Requirement

- python3
- numpy

## Reference

- [OpenAI Gym](https://github.com/openai/gym/blob/master/gym/envs/atari/atari_env.py)
- [ALE interface - Breakout](https://github.com/openai/atari-py/blob/master/atari_py/ale_interface/src/games/supported/Breakout.cpp)
- [BreakoutNoFrameskip-v4 video](https://youtu.be/o72FS5eqPNs)