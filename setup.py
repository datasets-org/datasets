#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from setuptools import setup

requirements = [line.rstrip('\n') for line in open('requirements.txt')]

setup(
    name='datasetstools',
    version='1.0.2',
    description='',
    long_description='Datasets tools',
    url='',
    author='Vit Listik',
    author_email='tivvit@seznam.cz',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    install_requires=requirements,
    keywords='dataset management',
    packages=[
        "datasets",
    ],
    entry_points={
        'console_scripts': [
            'datasets = datasets.dataset_cli:main',
        ]
    }
)
