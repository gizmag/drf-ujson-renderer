#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='drf_ujson',
    version='1.1',
    description='Dkango Rest Framework UJSON Renderer',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/drf-ujson-renderer',
    packages=find_packages(),
    install_requires=['django', 'ujson', 'djangorestframework']
)
