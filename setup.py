#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import setuptools

setup(
  name= "sigma",
  version = '0.1.0',
  description = "Language neutral source code files preprocessor.",
  author = "Grigory Petrov",
  author_email = "grigory.v.p@gmail.com",
  url = "http://bitbucket.org/eyeofhell/sigma",
  packages = [ 'sigma', 'sigma_gui' ],
  scripts = [ 'sigma.py', 'sigma_gui.py' ],
  classifiers=[
    'Development Status :: 1 - Prototype',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: GPLv3',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Utilities' ])

