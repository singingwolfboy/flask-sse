# coding=utf-8
from __future__ import unicode_literals

import sys
import re
from setuptools import setup, find_packages


version = ''
with open('flask_sse.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

install_requires = [
    "flask>=0.9",
    "redis",
    "six",
]

setup(
    name="Flask-SSE",
    version=version,
    description="Server-Sent Events for Flask",
    long_description=open('README.rst').read(),
    author="David Baumgold",
    author_email="david@davidbaumgold.com",
    url="https://github.com/singingwolfboy/flask-sse",
    packages=find_packages(),
    install_requires=install_requires,
    license='MIT',
    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Framework :: Flask',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ),
    zip_safe=False,
)
