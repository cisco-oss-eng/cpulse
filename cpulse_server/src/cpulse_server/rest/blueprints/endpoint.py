from flask import Blueprint, request, Response

page = Blueprint('endpoint', __name__)

@page.route('/cpulse/endpoint', methods=['GET'])
def endpoint():
    rc = 200
    #threading.Thread(target=tasks.netdelete, args=[simid]).run()
    mesg = 'ENDPOINT SUCCESS' if rc == 200 else 'FAILURE'
    return Response(mesg, status=200, mimetype='text/plain')

@page.route('/cpulse/endpoint/keystone', methods=['GET'])
def endpoint_keystone():
    rc = 200
    #threading.Thread(target=tasks.netdelete, args=[simid]).run()
    mesg = 'KEYSTONE SUCCESS' if rc == 200 else 'FAILURE'
    return Response(mesg, status=200, mimetype='text/plain')
