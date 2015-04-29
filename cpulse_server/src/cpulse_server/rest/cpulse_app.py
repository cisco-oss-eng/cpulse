from flask import Flask
import logging
from cpulse_server.infra.logger import getlog


cpulse_app = Flask(__name__)

# Set logger for cpulse 
errlog = '/var/log/cpulse/cpulse.log' 
fh = logging.handlers.RotatingFileHandler(errlog,
                                          maxBytes=20*1024*1024,
                                          backupCount=4)
fh.setLevel(logging.ERROR)
fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))
cpulse_app.logger.addHandler(fh)



@cpulse_app.route("/cpulse")
def hello():
    return "Hello World!"

##TODO: Fix SSL context, integrate with nginx
#if __name__ == "__main__":
#    log = getlog()
#    log.info("Hello Logger")
#    cpulse_app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')

