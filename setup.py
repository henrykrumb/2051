#!/usr/bin/env python

from setuptools import setup

setup(
    name='twentyfiftyone',
    version='1.0',
    description='',
    author='Henry Krumb',
    author_email='mail@henrykrumb.de',
    url='',
    packages=['twentyfiftyone'],
    entry_points='''
        [console_scripts]
        twentyfiftyone = twentyfiftyone:fmain
    '''
)
