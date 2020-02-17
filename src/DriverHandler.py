from .selenium_mod import (Options, webdriver)
from datetime import datetime, timedelta
from time import sleep
from . import debug_funcs as df
import os

DRIVER_HANDLER_DEBUG = True


class SafeStopSearchException(Exception):
    pass


class SearchRunningException(Exception):
    pass


class STATUS:
    RUNNING = "running"
    INITIALIZING = "initializing"
    LOADING = "loading"
    DELETED = "deleted"


class LOGS:
    NOTHING = "No logs available"
    LOADING_PAGE = "Loading page: "
    LOADING_COMPLETED = "Loading Completed: "
    SEARCH_FINISHED = "Search finished: "
    FOUND_PRODUCT = "found %i products on "
    ERROR = "Error occurred: "
    DRIVER_ALREADY_EXISTS = "Driver already exists "
    DRIVER_CREATED_AT = "Driver created at: "
    DRIVER_DELETED_AT = "Driver deleted at: "
    WAITING = "Waiting: "


class SellerData:
    def __init__(self, name, company, location, phone_num, whatsapp):
        self.name = name
        self.company = company
        self.location = location
        self.phone_num = phone_num
        self.whatsapp = whatsapp


class DriverHandler:
    def __init__(self, name, request, resources, pause_time=2):
        self.name = name
        self.request = request
        self.status = ""
        self.logs = ""
        self.set_logs(LOGS.NOTHING, "__init__")
        self.set_status(STATUS.DELETED, "__init__")
        self.sellers = []
        self.driver = None
        self.last_connected = datetime.now()
        self.parent = resources
        self.pause_time = pause_time
        self.run_search = False

    def set_status(self, status, called_by=""):
        self.status = status
        self.print_status(called_by)

    def set_logs(self, logs, called_by):
        self.logs = logs
        self.print_log(called_by)

    def load_page(self, url, wait_ele_xpath="", ele_count=1, refresh_also=False):
        func_name = "self.load_page"
        if not self.run_search:
            raise SafeStopSearchException("Stop loading")
        self.set_logs(LOGS.LOADING_PAGE + url, func_name)
        df.print_if_cond(DRIVER_HANDLER_DEBUG,
                         f"load_page(self={self},\n url={url},\n wait_ele_xpath={wait_ele_xpath},\n ele_count={ele_count},\n refresh_also={refresh_also})")
        sleep(self.pause_time)
        df.print_if_cond(DRIVER_HANDLER_DEBUG, "Network check. ")
        if self.status == STATUS.RUNNING:
            self.set_status(STATUS.LOADING, func_name)
        else:
            self.set_logs(LOGS.ERROR + "Cannot load page. Driver is not running", func_name)
        self.driver.wait_until_connected()
        self.driver.get(url)
        df.print_if_cond(DRIVER_HANDLER_DEBUG, "Loading started. Complete")
        if refresh_also:
            df.print_if_cond(DRIVER_HANDLER_DEBUG, "Refreshing page. ")
            self.driver.refresh()

        if wait_ele_xpath != "":
            for i in range(0, 5):
                wait_ele_found = len(self.driver.find_elements_by_xpath(wait_ele_xpath))
                df.print_if_cond(DRIVER_HANDLER_DEBUG,
                                 f"Wait Element found = {wait_ele_found}\tRequired Elements = {ele_count}\tLoop count = {i}")
                if wait_ele_found >= ele_count:
                    break
                sleep(1)
        self.set_status(STATUS.RUNNING, func_name)
        self.set_logs(LOGS.LOADING_COMPLETED, func_name)

    def __close_driver(self):
        func_name = "self.__close_driver"
        while self.status != STATUS.RUNNING:
            if self.status == STATUS.DELETED:
                self.set_logs(LOGS.ERROR + "Cannot close driver when it is not open.", func_name)
                return
        self.driver.quit()

    def search(self, query):
        df.pause_if_cond(DRIVER_HANDLER_DEBUG, "from parent")

    def print_log(self, called_by):
        df.print_if_cond(DRIVER_HANDLER_DEBUG, "print_log <- ", called_by, "\n", self.name+"'s logs:", self.logs)

    def print_status(self, called_by):
        df.print_if_cond(DRIVER_HANDLER_DEBUG, "print_status <-", called_by, "\n", self.name+"'s status: ", self.status)

    def create_d(self):
        func_name = "create_d"
        if isinstance(self.driver, webdriver.Chrome):
            self.set_logs(LOGS.ERROR + LOGS.DRIVER_ALREADY_EXISTS, func_name)
            # raise Exception(LOGS.ERROR + LOGS.DRIVER_ALREADY_EXISTS)
            return False
        self.set_status(STATUS.INITIALIZING, func_name)
        options = Options()
        driverpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
        if os.name == 'nt':
            self.driver = webdriver.Chrome(executable_path=driverpath+'.exe',
                                           options=options)
        else:
            self.driver = webdriver.Chrome(executable_path=driverpath,
                                           options=options)

        self.set_status(STATUS.RUNNING, func_name)
        self.set_logs(LOGS.DRIVER_CREATED_AT + str(datetime.now()), func_name)
        return True

    def start_search(self, query):
        func_name = "run search"
        print(self)
        while self.driver == STATUS.INITIALIZING:
            self.set_logs(LOGS.WAITING+"Browser is not completely open yet", func_name)
            sleep(1)
        if self.run_search:
            raise SearchRunningException("Search is already running")
        self.run_search = True
        try:
            self.search(query)
        except SafeStopSearchException:
            pass
        self.set_logs(LOGS.SEARCH_FINISHED, func_name)


    def run_until_connected(self):
        print(self)
        self.create_d()
        while True:
            if datetime.now() > self.last_connected + timedelta(seconds=10):
                self.delete_d()
                # users_resources.pop(self.request, None)
                self.parent.pop(self.request, None)
                break
            sleep(1)

    def update_last_connected(self):
        self.last_connected = datetime.now()
        return f"{self.name} Last Connected:  {self.last_connected}.\n"

    def delete_d(self):
        func_name = "self.delete_d"
        self.run_search = False
        self.__close_driver()
        self.driver = None
        self.set_status(STATUS.DELETED, func_name)
        self.set_logs(LOGS.DRIVER_DELETED_AT + str(datetime.now()), func_name)
        return True
        # else:
        #     self.logs = LOGS.ERROR + "Driver's instance did not find to deleted."
        #     self.print_log("delete_d")
        #     return False
