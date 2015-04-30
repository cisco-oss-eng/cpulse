from neutronclient.v2_0 import client as neutron_client
class NeutronHealth(object):
    def __init__(self, creds):
        self.neutronclient = neutron_client.Client(**creds)
    
    def neutron_agent_list(self):
        try:
            agent_list = self.neutronclient.list_agents()  
        except Exception as e:
            return (400, [])
        return (200, agent_list['agents'])
    