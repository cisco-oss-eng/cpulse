from novaclient.client import Client
class NovaHealth(object):
    """
    Provides all the necessary API
    for nova health Check
    """
    def __init__(self, creden):
        self.novaclient = Client(**creden)
    
    def nova_service_list(self):
        """
        Get the list of nova services
        """
        try:
            service_list = self.novaclient.services.list()
        except Exception as e:
            print e
            return (400, [])
        return (200, service_list)
