class cpulse_base:
    def __init__(self):
        pass

    def valid(self):
        return False

    def start(self):
        result = True 
        handle = 0x1
	return { 'result' : result,
                 'handle' : handle }

    def result(self):
        result = True 
	return result;

    def snapshot(self):
        result = True 
        handle = 0x1
	return { 'result' : result,
                 'handle' : handle }

    def verify(self):
        result = True 
        handle = 0x1
	return { 'result' : result,
                 'handle' : handle }
