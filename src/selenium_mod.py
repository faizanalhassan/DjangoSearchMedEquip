import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from . import debug_funcs as df
DEBUG = True


def is_internet_connected():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        print("Conecction Error")
        return False


def wait_until_connected(self):
    while True:
        if is_internet_connected():
            break
        else:
            print("Trying again to connect.")


def get_element_text(self, xpath, e=None):
    if e is not None:
        text = self.execute_script(f"""node = document.evaluate('{xpath}', arguments[0], null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;return node != null?node.innerText:'';""", e)
    else:
        text = self.execute_script(
            f"""node = document.evaluate("{xpath}", document, null,
             XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
            return node != null?node.innerText:'';""")
    return text.strip()


def get_element(self, xpath):
    if self.is_element_exists(xpath):
        return self.find_element_by_xpath(xpath)
    else:
        return None


def is_element_exists(self, xpath):
    try:
        self.find_element_by_xpath(xpath)
        return True
    except:
        return False


def click_element(self, xpath):
    if self.is_element_exists(xpath):
        self.execute_script(
            """var n = document.evaluate("%s", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;n.scrollIntoView();n.click()"""%xpath)
        return True
    return False


def get_element_attr(self, xpath, attr):
    value = ""
    if self.is_element_exists(xpath):
        value = self.execute_script("""return document.evaluate("%s", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue.getAttribute("%s");"""%(xpath, attr))
    return value if value is not None else ""


webdriver.Chrome.wait_until_connected = wait_until_connected
webdriver.Chrome.get_element_text = get_element_text
webdriver.Chrome.get_element = get_element
webdriver.Chrome.is_element_exists = is_element_exists
webdriver.Chrome.click_element = click_element
webdriver.Chrome.get_element_attr = get_element_attr
