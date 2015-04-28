from cpulse_server.infra.logger import getlog

if __name__ == "__main__":
    log = getlog()
    log.info("Hello Logger")
