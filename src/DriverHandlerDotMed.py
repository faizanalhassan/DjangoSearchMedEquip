from .DriverHandler import DriverHandler

PAUSE_TIME = 2
NAME = "dotmed.com"


class DriverHandlerDotMed(DriverHandler):
    def __init__(self, request, resources, query):
        super().__init__(NAME, request, resources, query, PAUSE_TIME)

    def search(self):
        page = 0
        while True:
            url = f"https://www.dotmed.com/listings/search/equipment.html?key={self.query}&offset={page * 15}"
            self.load_page(url, "//*[contains(@id,'listing_')]", 15)
            products = self.driver.find_elements_by_xpath(
                "//*[contains(@id,'listing_') and contains(@class,'listing-list')]/div//h4/a[contains(@href,'listing')]")
            products_links = []
            for product in products:
                link = product.get_attribute("href")
                products_links.append(link)
            for link in products_links:
                # if not do_continue_search(username,d_dotmed): break
                self.driver.load_page(link, "//*[text()='Seller Information']/..")
            next_page_links = self.driver.find_elements_by_xpath("")
            if len(next_page_links) == 0:
                break
