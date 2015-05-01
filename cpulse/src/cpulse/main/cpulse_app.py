import requests

def cpulse_check(args, server_url):
    print args.mode
    print args.service
    #req = server_url + '/cpulse/v1'
    req = server_url + '/cpulse/'+args.mode+'/'+args.service
#    req = server_url + '/'+args.mode+'/'+args.service
    print req
    ret = requests.get(req, verify=False)
    print ret.status_code
    if ret == 200:
        print ret.json()
    else:
        print "Something went wrong .."
    pass

def cpulse_result(args, server_url):
    print args.handle
    pass
