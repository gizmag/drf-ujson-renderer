#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='drf_ujson',
    version='2.0',
    description='Django Rest Framework UJSON Renderer',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/drf-ujson-renderer',
    packages=find_packages(),
    install_requires=['django', 'ujson', 'djangorestframework']
)
