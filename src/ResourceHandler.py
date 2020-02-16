from .DriverHandlerDotMed import DriverHandlerDotMed
from threading import Thread
from datetime import datetime
from time import sleep
users_resources = {}
run = True


def myconnect(request):
    while run:
        users_resources[request][0].last_connected = datetime.now()
        sleep(3)


def add_resource(request, query):
    if request in users_resources:
        return "Resource already existed"
    users_resources[request] = []
    d = DriverHandlerDotMed(request, users_resources, query)
    users_resources[request].append(d)
    Thread(target=users_resources[request][0].run_until_connected).start()
    Thread(target=myconnect, args=(request,)).start()
    while True:
        ans = input("Enter choice: ")
        users_resources[request][0].update_last_connected()
        if ans == "end":
            users_resources[request][0].run_search = False
            global run
            run = False
        elif ans == "s":
            Thread(target=users_resources[request][0].start_search).start()
