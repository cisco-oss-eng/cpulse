import argparse
import time
import configure
import credentials
import nova_api
import neutron_api
import keystone_api
import glance_api
import cinder_api
import logging
from random import randint

def _get_random_test_number():
    return str(randint(1000, 9999))

def create_tenant(keystone_instance,tenant_name):
    status, status_msg, tenant = keystone_instance.keystone_tenant_create(tenant_name)
    if  status == 200:
        if tenant:
            cpulse_log.debug("Tenant Name=%s Tenant ID=%s", tenant.name,
                                                            tenant.id)
        cpulse_log.critical("Tenant Create: OK")
        return tenant
    else:
        cpulse_log.critical("Tenant create Error:%s", status_msg)
        cpulse_log.critical("Tenant Create: FAIL")

def delete_tenant(keystone_instance,tenant):
    status, status_msg, tenant = keystone_instance.keystone_tenant_delete(tenant)
    if  status == 200:
        cpulse_log.critical("Tenant Delete: OK")
    else:
        cpulse_log.critical("Tenant delete Error:%s", status_msg)
        cpulse_log.critical("Tenant Delete: FAIL")

def create_image(glance_instance,image_name,image_url,container_format,disk_format):
    status, status_msg, image = glance_instance.glance_image_create(image_url,
                                                                image_name,
                                                                container_format,
                                                                disk_format)
    if  status == 200:
        cpulse_log.critical("Image Create: OK")
        return image
    else:
        cpulse_log.critical("Image create Error:%s", status_msg)
        cpulse_log.critical("Image Create: FAIL")

def create_server(nova_instance,server_name,image_name,flavor_name,network_id):
    status, status_msg, vm = nova_instance.nova_create_server(server_name,
                                                               image_name,
                                                               flavor_name,
                                                               network_id)
    if  status == 200:
        cpulse_log.critical("VM Create: OK")
        return vm
    else:
        cpulse_log.critical("VM create Error:%s", status_msg)
        cpulse_log.critical("VM Create: FAIL")

def delete_server(nova_instance,server_id):
    status, status_msg, vm = nova_instance.nova_delete_server(server_id)
    if  status == 200:
        cpulse_log.critical("VM Delete: OK")
    else:
        cpulse_log.critical("VM delete Error:%s", status_msg)
        cpulse_log.critical("VM Delete: FAIL")

def create_network(neutron_instance,network_name,subnet_cidr):
    status, status_msg, network = neutron_instance.network_create(network_name)
    if  status == 200:
        cpulse_log.critical("Network Create: OK")
    else:
        cpulse_log.critical("Network create Error:%s", status_msg)
        cpulse_log.critical("Network Create: FAIL")
        return ""

    status, status_msg, subnetwork = neutron_instance.subnet_create(network['network']['id'],subnet_cidr)
    if  status == 200:
        cpulse_log.critical("Subnet Create: OK")
    else:
        cpulse_log.critical("Subnet create Error:%s", status_msg)
        cpulse_log.critical("Subnet Create: FAIL")
        return ""
    return network

def delete_network(neutron_instance,network):
    status, status_msg, network = neutron_instance.network_delete(network['network']['id'])
    if  status == 200:
        cpulse_log.critical("Network Delete: OK")
    else:
        cpulse_log.critical("Network delete Error:%s", status_msg)
        cpulse_log.critical("Network Delete: FAIL")
        return ""

def functional_check_start(config_api):
    print config_api
    creds = cred.get_credentials()
    creds_nova = cred.get_nova_credentials_v2()
    Test_data = {}
    Api_data = {}

    test_number = _get_random_test_number()
    tenant_name = config_api['prefix'] + '_tenant' + test_number
    network_name = config_api['prefix'] + '_network' + test_number
    vm_name = config_api['prefix'] + '_vm' + test_number
    glance_name = config_api['prefix'] + '_image' + test_number
    volume_prefix = config_api['prefix'] + '_volume' + test_number
    cpulse_log.critical("Starting Functional Test %s",test_number)

    keystone_instance = keystone_api.KeystoneHealth(creds)

    #Creating Tenant
    tenant = create_tenant(keystone_instance,tenant_name)
    Test_data['tenant'] = tenant

    #Changing Tenant to the New Tenant Number
    creds['tenant_name'] = tenant.name
    creds_nova['project_id'] = tenant.name
    keystone_instance = keystone_api.KeystoneHealth(creds)
    neutron_instance = neutron_api.NeutronHealth(creds)
    nova_instance = nova_api.NovaHealth(creds_nova)
    cinder_instance = cinder_api.CinderHealth(creds_nova)
    glance_instance = glance_api.GlanceHealth(keystone_instance)

    #Creating Network and subnet
    network = create_network(neutron_instance,network_name,config_api['network_cidr'])
    Test_data['network'] = network

    #Uploading image to glance
    Image = create_image(glance_instance,glance_name,
                                                    config_api['image_url'],
                                                    config_api['image_container_format'],
                                                    config_api['image_disk_format'])

    Test_data['server'] = []
    #Creating 2 servers
    server1_name = vm_name + "_1"
    server2_name = vm_name + "_2"
    server1 = create_server(nova_instance,server1_name,Image.name,config_api['flavor'],network['network']['id'])
    server2 = create_server(nova_instance,server2_name,Image.name,config_api['flavor'],network['network']['id'])
    Test_data['server'].append(server1)
    Test_data['server'].append(server2)


    #Cleanup Routines
    if Test_data['server']:
        for server in Test_data['server']:
            delete_server(nova_instance,server.id)
    if Test_data['network']:
        delete_network(neutron_instance,Test_data['network'])

    if Test_data['tenant']:
        delete_tenant(keystone_instance,Test_data['tenant'])


if __name__ == '__main__':
    default_cfg_file = "cfg_functional.yaml"
    parser = argparse.ArgumentParser(description="Functional Check status check")
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
    parser.add_argument('-d', '--debug', dest='debug',
                        default=False,
                        action='store_true',
                        help='debug level',
                        )

    (opts, args) = parser.parse_known_args()
    config_api = configure.Configuration.from_file(default_cfg_file).configure()
    cred = credentials.Credentials(opts.rc, opts.pwd, opts.no_env)

    cpulse_log = logging.getLogger()
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    cpulse_log.addHandler(ch)
    ch.setFormatter(formatter)

    if opts.debug:
        cpulse_log.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    functional_check_start(config_api)
