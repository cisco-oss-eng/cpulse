import requests

def cpulse_check(args, server_url):
    print args.mode
    req = server_url + '/cpulse/v1'
    print req
    ret = requests.get(req, verify=False)
    print ret.status_code
    print ret.json()
    pass

def cpulse_result(args, server_url):
    print args.handle
    pass
