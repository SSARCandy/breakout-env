from setuptools import setup, find_packages

def read_readme():
  with open('README.md') as f:
    return f.read()

setup(
  name = 'breakout_env',
  packages=find_packages(),
  version='1.0.3',
  description = 'A configurable Breakout environment for reinforcement learning',
  long_description = read_readme(),
  author = 'SSARCandy',
  author_email = 'ssarcandy@gmail.com',
  license = 'MIT',
  url = 'https://github.com/SSARCandy/breakout-env', # use the URL to the github repo
  # download_url = 'https://github.com/SSARCandy/breakout-env/archive/1.0.0.tar.gz', # I'll explain this in a second
  keywords = ['game', 'learning', 'evironment'], # arbitrary keywords
  classifiers = [],
  install_requires=['numpy>=1.1', 'distribute'],
  include_package_data=True
)