#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import sigma.info

setuptools.setup(
  name         = sigma.info.NAME_SHORT,
  version      = sigma.info.VER_TXT,
  description  = "Language neutral source code files preprocessor.",
  author       = "Grigory Petrov",
  author_email = "grigory.v.p@gmail.com",
  url          = "http://bitbucket.org/eyeofhell/sigma",
  packages     = [ 'sigma', 'sigma_gui' ],
  entry_points = {
    'console_scripts' : [
      'sigma = sigma:main',
      'sigmag = sigma_gui:main',
    ]
  },
  classifiers  = [
    'Development Status :: 1 - Prototype',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: GPLv3',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Utilities'
  ],
)

