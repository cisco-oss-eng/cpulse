import argparse
import configure
import credentials
import nova_api
import neutron_api
import keystone_api
import glance_api

def nova_endpoint_check(nova_instance):
    status, message, service_list = nova_instance.nova_service_list()
    if  status == 200:
        for service in service_list:
            print "Binary=%s Host=%s Zone=%s Status=%s State=%s" %(service.binary, service.host,
                                                                   service.zone, service.status,
                                                                   service.state)
    else:
        print "Nova service list error:%s" %(message)
        
def keystone_endpoint_check(keystone_instance):
    status, message, service_list = keystone_instance.keystone_service_list()
    if status == 200:
        for service in service_list:
            print "Service=%s enabled=%s" %(service.name, service.enabled)
    else:
        print "Keystone service list error:%s" %(message)
    

def neutron_endpoint_check(neutron_instance):
    status, message, agent_list = neutron_instance.neutron_agent_list()
    if status == 200:
        for agent in agent_list:
            print "Agent=%s Host=%s Alive=%s admin_state_up=%s" %(agent['binary'], agent['host'],
                                                                  agent['alive'], agent['admin_state_up'])
    else:
        print "neutron agent list error:%s" %(message)

def glance_endpoint_check(glance_instance):
    status, message, image_list = glance_instance.glance_image_list()
    if status == 200:
        for image in image_list:
            print "Image=%s Status=%s" %(image.name, image.status)
    else:
        print "Image List error:%s" %(message)


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
    neutron_instance = neutron_api.NeutronHealth(creds)
    keystone_instance = keystone_api.KeystoneHealth(creds)
    glance_instance = glance_api.GlanceHealth(keystone_instance)
    # Check the health of various endpoints
    nova_endpoint_check(nova_instance)
    neutron_endpoint_check(neutron_instance)
    keystone_endpoint_check(keystone_instance)
    glance_endpoint_check(glance_instance)
    
    


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
    
    