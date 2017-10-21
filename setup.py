#!/usr/bin/env python

from setuptools import setup, find_packages
import os.path

setup(name='tap-github-stars',
      version='0.0.1',
      description='Singer.io tap for extracting Stargazers from GitHub',
      author='Fishtown Analytics',
      url='http://fishtownanalytics.com',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_github_stars'],
      install_requires=[
          'singer-python==0.2.1',
          'backoff==1.3.2',
          'requests',
          'python-dateutil==2.6.0',
      ],
      entry_points='''
          [console_scripts]
          tap-github-stars=tap_github_stars:main
      ''',
      packages=['tap_github_stars']
)
