from argparse import ArgumentError, SUPPRESS, ArgumentParser, \
    RawDescriptionHelpFormatter, Action
import ConfigParser
import getpass
import os
import sys
sys.path.append("/home/cisco/cpulse/cpulse/src")
from cpulse.main.cpulse_app import cpulse_check, cpulse_result



def initialise():
    ''' Determine the server IP'''
    confparser = ConfigParser.ConfigParser()
    server_conf = os.path.expanduser('~/.cpulse-backend')
    if os.path.exists(server_conf):
        confparser.read(server_conf)
        host = confparser.get('REST', 'host')
        port = confparser.get('REST', 'port')
        server_ip_port = [ host, port ]
        print "server IP and Port info "
        return server_ip_port

class versionAction(Action):

    def __call__(self, verparser, namespace, values, option_string=None):
        initialise(None)
        version = "1.2.3"
        print(version)
        sys.exit(0)

def cli(package_type=None, argv=None):  
    '''Parse Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    try:
        # Setup argument 
        parser = ArgumentParser(
                description='Cloud Pulse Openstack Health Check Tool',
                formatter_class=RawDescriptionHelpFormatter)


        common_parser = ArgumentParser(add_help=False)
        common_parser.add_argument('-l', '--loglevel', metavar='LEVEL',
        # loglevel can be one of ['debug','info','warning','error','critical']
                 help= SUPPRESS,
                 default='info')

        subparsers = parser.add_subparsers(help='Sub-commands')
        check_parser = subparsers.add_parser('check',
                   parents=[common_parser],
                   help='Run health check test')

        result_parser = subparsers.add_parser('result',
                   parents=[common_parser],
                   help='Print health check result')


        check_parser.add_argument('-m', '--mode', dest='mode',
                                     metavar='NAME',
                                     default=False, required=True,
                                     help='Supported test modes are Operator, Endpoint, Functional, Comprehensive')

        check_parser.add_argument('-s', '--service', dest='service',
                                     metavar='NAME', default='all',
                                     help='Service needs to be nova, neutron, cinder, glance, keystone, all')

        check_parser.set_defaults(func = cpulse_check)

        result_parser.add_argument('-i', '--id', dest='handle',
                                     metavar='NAME',
                                     default=False, required=True,
                                     help='identifier returned by check, or latest for last run test')

        result_parser.set_defaults(func = cpulse_result)

        # Process arguments
        args = parser.parse_args()
        server_ip_port = initialise()
        server_url = 'https://' + server_ip_port[0] + ':' + server_ip_port[1] 
        return args.func(args, server_url)

    except ArgumentError as err:
        print "Argument error "
        return 1
    except OSError as err:
        print "System error " . format(err.errno, err.strerror)
        return 1
    except IOError as err:
        print "File Error " . format(err.errno, err.strerror)
        return 1

if __name__ == "__main__":
    sys.exit(cli())

