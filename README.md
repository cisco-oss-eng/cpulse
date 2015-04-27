Cloud Pulse
------------
NFV applications have stringent SLA, they need to be highly available with an uptime of 99.9 (99).
NFV availability depends on the cloud infrastructure and hence they need to be aware of health of openstack service.
when the infrastructure failure is detected early, these applications can be moved to a different cloud and the cloud operators 
can be notified . The key take away here is catching and handling failures before NFV customer experiences an application failure.

when is openstack healthy ?
----------------------------
a. All openstack services receives queries and replies back with an expected result.
b. Packets can be sent and received on tenant and external network

Requirements
------------
Provide a tool that checks the health of the cloud.
1. Should be light weight, non disruptive and less  resource intensive.
2. Should provide configurable functional testing
3. Should verify resource states after openstack upgrade
4. Should work on all openstack installs, i.e it should be agnostic to openstack distribution and various deployment models.
5. Should work for both tenants and operators
6. Provide both CLI and API.

Different type of health checks
--------------------------------
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
-------------------------
   Application can make use of endpoint, comprehensive, functional and upgrade checks. Application can snapshot the resources before upgrade and then check there state after the upgrade. Cloud Pulse itself can be run as a tenant-vm, which then can provide REST-API access to other NFV, VNFM, NFVO applications.

Operator health check
----------------------
  Operators can install cloud-pulse in one of the controllers directly or using docker container. They should be able to run all of the health checks listed above.



