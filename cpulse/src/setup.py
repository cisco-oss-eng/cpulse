from datetime import date
from setuptools import setup
from glob import glob
import os
import sys


PKGVERSION = '0.1.0'

PACKAGES = ['cpulse',
            'cpulse.infra',
            'cpulse.main',
           ]

DATA = {}
ENTRY_POINTS = { 'console_scripts': ['cpulse=cpulse.main.cpulse_cli:main'] }
REQUIRES = ['requests']
setup(
      name='cpulse',
      version=PKGVERSION,
      description='Cloud Pulse',
      long_description='',
      author='cpulse-dev',
      author_email='cpulse_server-dev@cisco.com',
      url='http://github.com/cisco-oss-eng/cpulse',
      packages=PACKAGES,
      package_data=DATA,
      install_requires=REQUIRES,
      entry_points=ENTRY_POINTS,
      )
