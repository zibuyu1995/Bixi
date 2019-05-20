#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup


INSTALL_REQUIRES = [
    'uvloop',
    'mode',
    'click',
    'croniter',
    'asyncpg'
]

setup(
    name='mtasks',
    version='1.1',
    description='Asynchronous timing tasks',
    author='Mousse',
    author_email='zibuyu1995@gmail.com',
    url='http://www.eds1995.com/',
    platforms=['any'],
    license='MIT',
    install_requires=['aiohttp', 'click'],
    python_requires='>=3.6.0',
    keywords=[
        'asyncio',
        'timer task'
    ],
    entry_points={
        'console_scripts': [
            'mtasks = mtasks.cli:start',
        ],
    },
)
