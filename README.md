Cloud Pulse
------------
NFV applications have stringent SLA, they need to be highly available with an uptime of 99.9 (99).
NFV availability depends on the cloud infrastructure and hence they need to be aware of health of openstack service.
when the infrastructure failure is detected early, these applications can be moved to a different cloud and the cloud operators 
can be notified . The key take away here is catching and handling failures before NFV customer experiences an application failure.

when is openstack healthy ?
a. All openstack services receives queries and replies back with an expected result.
b. Packets can be sent and received on tenant and external network

Goal:
Provide a tool that checks the health of the cloud.
1. Should be light weight, non disruptive and less  resource intensive.
2. Should provide configurable functional testing
3. Should verify resource states after openstack upgrade
4. Should work on all openstack installs, i.e it should be agnostic to openstack distribution and various deployment models.
5. Should work for both tenants and operators
6. Provide both CLI and API.

Different type of health checks:
1. Operator check*
   a. Check all services are running and listening on the ports  
   b. check the cluster status of infra components rabbit and percona (mysql ‘wsrep’ and rabbitmqctl cluster_status)
   c. If Openstack is in HA mode, test the HAProxy and each of the services behind the HAProxy (run 'a' and 'b’)
   d. If pacemaker is installed, use 'crm status' or  ‘pcs status'

Requires cloud-admin and operator access.

2. Endpoint check
   a. keystone service-list
   b. glance image-list
   c. cinder list
   d. nova list
   e. neutron net-list
   f. login to horizon page 

3. Functional check
   a. Create tenant, create network, upload an image, create two VMs and run ping between the VMs.
   b. Create VM, create volume, attach volume to the VM.
   c. detach VM, delete volume and delete VM
   d. Clean up all resources

4. Comprehensive health check
   a. Create VM on each compute node and ping the gateway.
   b. Determine max MTU and check jumbo packets (optional)
   c. Check security groups (ping, ssh and http traffic)

5. Upgrade check
   a. Create or snapshot the state of existing openstack resources such as tenants/routers/VMs/Loadbalancers
   b. After upgrade check if the created/snapshotted resources are in operational state
   c. Check security groups after upgrade (ping, ssh and http)

Application health check
   Application can make use of endpoint, comprehensive, functional and upgrade checks. Application can snapshot the resources before upgrade and then check there state after the upgrade. Cloud Pulse itself can be run as a tenant-vm, which then can provide REST-API access to other NFV, VNFM, NFVO applications.

Operator health check
  Operators can install cloud-pulse in one of the controllers directly or using docker container. They should be able to run all of the health checks listed above.

Design:
Cloud pulse shall run as a web-service, it can be installed on container, virtual or physical machine, it shall provide REST API's to run each of the health checks, and they shall be non-blocking. In addition, the checks shall run at regular intervals as configured in the configuration file. 

Pre-req:
For operational health check, password less SSH setup from controller to other controller/compute servers.

Input:
a. Openstack API access (admin or tenant)
b. Service map*  (optional, details below)


API:
Webservice exposing the following API

POST /cpulse/check
Parameters
type = operation, endpoint, function, comprehensive, upgrade, all
Returns
{
   handle : "hhh"
}

GET /cpulse/result
Parameters
handle = handle
Returns
{ 
    timestamp : "ttt"
    handle : "handle"
    tests_failed : [
			{
			    glance-api : "details of failure "
			},
			{
			    cinder : "details of failure "
                        }
                   ]
    tests_passed : [ neutron, keystone ]
}

Snapshot API is used to create or snapshot  resources before the upgrade. This method is called before an upgrade with create option set to True or False. When create option is set to False, existing resources of the tenant are snapshotted, so that the resource state can be verified after the upgrade. When create option is True, resources passed as JSON struct defined below is created before the upgrade.

POST /cpulse/snapshot
Parameters
create = True
resources = {
   image: [i1, i2, i3]
   vm : [vm1, vm2, vm3]
   net : [net1, net2, net3]
   router: [r1, r2]
   connections: { [vm1, vm2], [vm2, vm3] }
}

Returns 
{
   timestamp : "ttt"
   handle : "hhh"
   resources = {
        image: [i1, i2, i3]
        vm : [vm1, vm2, vm3]
        net : [net1, net2, net3]
        router: [r1, r2]
        connections: { [vm1, vm2], [vm2, vm3] }

}

Deliverables:
a. Osh client python package
b. Osh server python package 
c. VM image (and docker ?) with osh-server and client pre-installed.

Brief Implementation detail:
1. Server: health service runs as webservice for API ( nginx, uwsgi, python-flask )

a. Python package shall be created for  cloudpulse server 
b. Package installer shall install nginx/uwsgi and configure them
c. Create seperate flask blueprint for operator, functional (include endpoint), comprehensive and upgrade
d. Tests should be modular, so that operator or application shall decide the tests that need to run and the test frequency.
       Configuration:
       /etc/oscheck.conf
       #service type : runinterval
       # Ability to set different time intervals for different health checks
       # typically wait long enough before resource intensive test
       # -1, indicates the check should not be run
       osoperator = 60ms
       osendpoint = 120ms
       osfunc = 180ms
       oscomp = 600ms

2. Client: Client CLI sends http requests to the server, can be run from remote locations
a. Python package shall be created for  cloudpulse server 
b. cpulse can be run from remote location
c. cpulse server IP and port information shall be configurable using config file (~.cpulserc)
d. CLI supported
   1. cpulse check [operator, functional, endpoint, comprehensive ]
   2. cpulse upgrade [snapshot | create]
   3. cpulse result handle

service_map example (from canonical install):
    Cinder-units:
      cinder/0:
        agent-state: started
        public-address: 10.20.0.100
      cinder/1:
        agent-state: started
        public-address: 10.20.0.102
      cinder/2:
        agent-state: started
        public-address: 10.20.0.101
   Ceph-units:
      ceph/0:
        agent-state: started
        public-address: cvpn-compute2.maas
      ceph/1:
        agent-state: started
        public-address: cvpn-compute1.maas
      ceph/2:
        agent-state: started
        public-address: cvpn-compute0.maas

