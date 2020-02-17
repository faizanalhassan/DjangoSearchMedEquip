from .DriverHandlerDotMed import DriverHandlerDotMed
from threading import Thread
from datetime import datetime
from time import sleep
users_resources = {}
run = True


def add_resource(identifier):
    if identifier in users_resources:
        return "Resource already existed"
    users_resources[identifier] = []
    users_resources[identifier].append(DriverHandlerDotMed(identifier, users_resources))
    Thread(target=users_resources[identifier][0].run_until_connected).start()
    # add other drivers here
