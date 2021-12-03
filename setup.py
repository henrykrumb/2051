#!/usr/bin/env python

from setuptools import setup

setup(
    name='twentyfiftyone',
    version='1.0',
    description='',
    author='Henry Krumb',
    author_email='mail@henrykrumb.de',
    url='',
    include_package_data=True,
    package_data={
        'twentyfiftyone': [
            'resources/*',
            'resources/assets/*/*',
            'resources/fonts/*',
            'resources/rooms/*',
        ]
    },
    packages=['twentyfiftyone'],
    entry_points='''
        [console_scripts]
        twentyfiftyone = twentyfiftyone:fmain
    '''
)
