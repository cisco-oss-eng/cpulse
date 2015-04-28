from flask import Flask
from cpulse_server.infra.logger import getlog


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

##TODO: Fix SSL context, integrate with nginx
if __name__ == "__main__":
    log = getlog()
    log.info("Hello Logger")
    app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')

