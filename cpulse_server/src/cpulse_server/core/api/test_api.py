import argparse
import configure
import credentials
import nova_api
import neutron_api

def health_check_start():
    """
    Function that triggers the health Check of
    various Openstack components
    """
    # Create the keystone client for all operations
    creds = cred.get_credentials()
    creds_nova = cred.get_nova_credentials_v2()
    # Create the clients for all components
    
    nova_instance = nova_api.NovaHealth(creds_nova)
    message, services_list = nova_instance.nova_service_list()
    if  message == "success":
        for service in services_list:
            print "Binary=%s Host=%s Zone=%s Status=%s State=%s" %(service.binary, service.host,
                                                                   service.zone, service.status,
                                                                   service.state)
    else:
        print "Nova service list error:%s" %(message)

    neutron_instance = neutron_api.NeutronHealth(creds)
    message, agent_list = neutron_instance.neutron_agent_list()
    if message == "success":
        for agent in agent_list:
            print "Agent=%s Host=%s Alive=%s admin_state_up=%s" %(agent['binary'], agent['host'],
                                                                  agent['alive'], agent['admin_state_up'])
    else:
        print "neutron agent list error:%s" %(message)
    

if __name__ == '__main__':
    default_cfg_file = "cfg_api.yaml"
    parser = argparse.ArgumentParser(description="Health Check status check")
    parser.add_argument('-r', '--rc', dest='rc',
                        action='store',
                        help='source Openstack credentials from rc file',
                        metavar='<openrc_file>')
    parser.add_argument('-p', '--password', dest='pwd',
                        action='store',
                        help='Openstack password',
                        metavar='<password>')
    parser.add_argument('--noenv', dest='no_env',
                        default=False,
                        action='store_true',
                        help='do not read env variables')
    (opts, args) = parser.parse_known_args()
    config_api = configure.Configuration.from_file(default_cfg_file).configure()
    cred = credentials.Credentials(opts.rc, opts.pwd, opts.no_env)
    health_check_start()
    
    