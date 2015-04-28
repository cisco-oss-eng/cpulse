
from datetime import date
from distutils.core import setup
from glob import glob
import os
import sys


PKGVERSION = '0.1.0'

PACKAGES = ['cpulse_server',
            'cpulse_server.infra',
            'cpulse_server.rest',
            'cpulse_server.rest.blueprints']

#DATA = {'cpulse_server.parser': ['schema/*', 'template/*'],
#        'cpulse_server.action': ['internal_config'],
#        'cpulse_server.vm.test': ['*.xml'],
#        'cpulse_server.rest.test':['*.txt']}
DATA = {}
#FILES = [('share/doc/python-cpulse_server', glob('doc/*.pdf')),
#         ('/etc/cpulse_server', ['data/cpulse_serverrc']),
#         ('/etc/init', ['cpulse_server/infra/vmcwebsvc.conf']),
#         ('/etc/sudoers.d', ['cpulse_server/infra/vmcperms'])]

#SCRIPTS = ['cpulse_server/rest/cpulse_server',
#           'cpulse_server/rest/logscrubber']

#REQUIRES = ['lxml', 'libxml2', 'libvirt', 'guestfs', 'pyvmomi']

SCRIPTS = []
REQUIRES = []
FILES = []

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
