from neutronclient.v2_0 import client as neutron_client
from neutronclient.common.exceptions import NeutronException
class NeutronHealth(object):
    def __init__(self, creds):
        self.neutronclient = neutron_client.Client(**creds)
    
    def neutron_agent_list(self):
        try:
            agent_list = self.neutronclient.list_agents()  
        except (NeutronException,Exception) as e:
            return (e.message, [])
        return ("success", agent_list['agents'])