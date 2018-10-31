#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='iotcsfunctionsAG',
    version='1.0.9',
    packages=find_packages(),
    install_requires=['dill','numpy','pyarrow','s3fs'],
)
