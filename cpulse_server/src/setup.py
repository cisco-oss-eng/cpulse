
from datetime import date
from distutils.core import setup
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

#DATA = {'cpulse_server.parser': ['schema/*', 'template/*'],
#        'cpulse_server.action': ['internal_config'],
#        'cpulse_server.vm.test': ['*.xml'],
#        'cpulse_server.rest.test':['*.txt']}
DATA = {}
FILES = [
         ('/etc/init', ['cpulse_server/infra/cpulsesvc.conf'])
        ]

SCRIPTS = ['cpulse_server/infra/cpulsesvc']

#REQUIRES = ['lxml', 'libxml2', 'libvirt', 'guestfs', 'pyvmomi']

REQUIRES = []

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
      requires=REQUIRES,
      )
