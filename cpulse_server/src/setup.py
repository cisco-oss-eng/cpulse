from datetime import date
from setuptools import setup
from glob import glob
import os
import sys


PKGVERSION = '0.1.0'

PACKAGES = ['cpulse_server',
            'cpulse_server.infra',
            'cpulse_server.rest',
            'cpulse_server.rest.blueprints',
            'cpulse_server.core',
            'cpulse_server.core.api',
            'cpulse_server.core.operator',
            'cpulse_server.extensions',
           ]
DATA = {}
FILES = [
         ('/etc/init', ['cpulse_server/infra/cpulsesvc.conf'])
        ]

SCRIPTS = ['cpulse_server/infra/cpulsesvc']
REQUIRES = ['flask',
            'pyOpenSSL',
            'python-novaclient',
            'python-openstackclient',
            'python-keystoneclient',
            'python-glanceclient',
            'python-cinderclient',
            'python-swiftclient',
            'python-ceilometerclient',
            'python-heatclient',
            'python-neutronclient']
setup(
      name='cpulse_server',
      version=PKGVERSION,
      description='Cloud Pulse',
      long_description='',
      author='cpulse-dev',
      author_email='cpulse_server-dev@cisco.com',
      url='http://github.com/cisco-oss-eng/cpulse',
      packages=PACKAGES,
      package_data=DATA,
      data_files=FILES,
      scripts=SCRIPTS,
      install_requires=REQUIRES,
      )
