# -*- coding: utf-8 -*-
'''
:copyright: (c) 2019 by Michael Krukov
:license: MIT, see LICENSE for more details.
'''

import sys

import setuptools


VERSION = '0.1.1'


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='sanic_restful_resources',
    version=VERSION,
    author='Michael Krukov',
    author_email='krukov.michael@ya.ru',
    keywords=['restful', 'rest', 'api', 'sanic', 'web', 'server'],
    description='The library for writing RESTful APIs with sanic',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/michaelkrukov/sanic-restful-resources',
    packages=setuptools.find_packages(exclude=('examples',)),
    install_requires=[
        'sanic>=19.12.2',
        'schematics>=2.1.0',
        'PyJWT>=1.7.1',
        'sanic-jwt-extended==1.0.dev5',
    ],
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ],
)
