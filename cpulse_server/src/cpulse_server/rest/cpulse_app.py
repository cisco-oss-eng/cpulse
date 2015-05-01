from flask import Flask
import logging
import json
import pkgutil
from flask import Blueprint, request, Response 
from cpulse_server.infra.logger import getlog
import cpulse_server.rest.blueprints


cpulse_app = Flask(__name__)

# Import the blueprints from the blueprints package
package = cpulse_server.rest.blueprints
prefix = package.__name__ + "."
for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
    _module = __import__(modname, globals(), locals(), ['page'], -1)
    print "BluePrint Registered .."
    cpulse_app.register_blueprint(_module.page)


# Set logger for cpulse 
errlog = '/var/log/cpulse/cpulse.log' 
fh = logging.handlers.RotatingFileHandler(errlog,
                                          maxBytes=20*1024*1024,
                                          backupCount=4)
fh.setLevel(logging.ERROR)
fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))
cpulse_app.logger.addHandler(fh)

@cpulse_app.route('/cpulse/v1', methods=['GET'])
def version():
    data = {
         # pylint: disable=E1103
         'Version': 0.1, 
         'Host': request.host,
         'authenticated': True if request.remote_user else False,
         'Remote-address': request.remote_addr,
         }
    js = json.dumps(data, indent=4, sort_keys=True)
    return Response(js, status=200, mimetype='application/json')


@cpulse_app.route("/cpulse")
def hello():
    return "Hello World!"

##TODO: Fix SSL context, integrate with nginx
#if __name__ == "__main__":
#    log = getlog()
#    log.info("Hello Logger")
#    cpulse_app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')

