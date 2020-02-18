from .DriverHandler import DriverHandler, create_seller_dict
from . import debug_funcs as df

DEBUG = True
PAUSE_TIME = 2
NAME = "medwow.com"


class DriverHandlerMedWow(DriverHandler):
    def __init__(self, user_id, resources):
        super().__init__(user_id, NAME, resources, PAUSE_TIME)

    def search(self, query):
        self.sellers.append(create_seller_dict("Test", "Test where", "Nope", "000", "09090"))
