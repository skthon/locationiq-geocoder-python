#/usr/bin/env python

from setuptools import setup, find_packages
import sys

if sys.version_info <= (2, 4):
  error = 'Requires Python Version 2.5 or above... exiting.'
  print >> sys.stderr, error
  sys.exit(1)

requirements = [
    'requests>=2.11.1'
    'pytest==3.0.3'
]

setup(
    name='locationiq',
    version='0.0.1',
    description='Python client library for LocationIQ Gecoding Services',
    scripts=[],
    author="saikiran ch",
    author_email="saikiranchavan@gmail.com",
    url='https://github.com/skthon/locationiq-geocoder-python',
    packages=['locationiq'],
    license='Apache 2.0',
    platforms='Posix; MacOS X; Windows',
    setup_requires=requirements,
    install_requires=requirements,
)