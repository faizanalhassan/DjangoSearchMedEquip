from .DriverHandler import DriverHandler, SellerData
from . import debug_funcs as df
DEBUG = True
PAUSE_TIME = 2
NAME = "dotmed.com"


class DriverHandlerDotMed(DriverHandler):
    def __init__(self, request, resources):
        super().__init__(NAME, request, resources, PAUSE_TIME)

    def search(self, query):
        page = 0
        while True:
            url = f"https://www.dotmed.com/listings/search/equipment.html?key={query}&offset={page * 15}"
            self.load_page(url, "//*[contains(@id,'listing_')]", 14)
            products = self.driver.find_elements_by_xpath(
                "//*[contains(@id,'listing_') and contains(@class,'listing-list')]/div//h4/a[contains(@href,'listing')]")
            products_links = []
            for product in products:
                link = product.get_attribute("href")
                df.print_if_cond(DEBUG, link)
                products_links.append(link)
            for link in products_links:
                self.load_page(link, "//*[text()='Seller Information']/..")
                name = self.driver.get_element_text(
                    "//*[text()='Seller Information']/../div/div/span[./following-sibling::*]")
                company_name = self.driver.get_element_text(
                    "//*[text()='Seller Information']/../div/div/span[not(./following-sibling::*)]")
                location = self.driver.get_element_text(
                    "//*[text()='Seller Information']/../div//span[contains(text(),'Location :')]")\
                    .replace("Location :", "")
                phone_num = self.driver.get_element_text(
                    "//*[text()='Seller Information']/../div//span[contains(text(),'Phone :')]")\
                    .replace("Phone :", "")
                whatsapp = self.driver.get_element_text(
                    "//*[text()='Seller Information']/../div//li[.//*[contains(@class,'fa fa-whatsapp')]]")
                seller_data = SellerData(name, company_name, location, phone_num, whatsapp)
                df.print_if_cond(DEBUG, "Seller's Data: ",seller_data)
                self.sellers.append()

            next_page_links = self.driver.find_elements_by_xpath("//*[@class='page-item']//*[contains(text(), 'Next')]")
            if len(next_page_links) == 0:
                break
