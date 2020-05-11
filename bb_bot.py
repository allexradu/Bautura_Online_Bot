from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException


def sub_category_xpath(index):
    return '//*[@id="narrow-by-list"]/dd[1]/ol/li[{index}]/a'.format(index = index)


def product_xpath(index):
    return '/html/body/main/div/div/div/div[2]/div[6]/ul/li[{index}]/div/div/div[1]/p/a'.format(index = index)


def find_sub_category_range_size(self):
    range_size = 1

    while True:
        try:
            elem = self.driver.find_element_by_xpath(sub_category_xpath(range_size))
            print(elem.text)
            range_size += 1
        except NoSuchElementException:
            break
        else:
            print('pass')
    return range_size


def find_product_range_size(self):
    range_size = 1

    while True:
        try:
            elem = self.driver.find_element_by_xpath(product_xpath(range_size))
            print(elem.text)
            range_size += 1
        except NoSuchElementException:
            break
        else:
            print('pass')

    return range_size


def main_category_loop(self, delay):
    for main_category_index in range(2, 9):
        # pressing the main category in the loop
        elem = self.driver.find_element_by_css_selector(
            'ul#nav>li:nth-of-type({main_category_index})>a'.format(main_category_index = main_category_index))
        main_category = elem.text
        print(main_category)
        self.driver.execute_script("arguments[0].click();", elem)

        sub_category_loop(self, find_sub_category_range_size(self), delay)


def sub_category_loop(self, loop_size, delay):
    for i in range(loop_size):
        # clicking on the fist sub-category
        # //*[@id="narrow-by-list"]/dd[1]/ol/li[THIS IS THE PARAMETER THAT CHANGES]/a
        try:
            element = self.driver.find_element_by_xpath(sub_category_xpath(i))
            sub_category = element.text
            print(sub_category)
            element.click()
            sleep(delay)
        except NoSuchElementException:
            continue

        product_page_loop(self, delay)


def product_page_loop(self, delay):
    while True:
        for i in range(find_product_range_size(self) - 1):
            # getting the first product element, getting the title and clicking on the fist product
            # /html/body/main/div/div/div/div[2]/div[6]/ul/li[THIS IS THE PARAMETER THAT CHANGES]/div/div/div[1]/p/a
            element = self.driver.find_element_by_xpath(
                '/html/body/main/div/div/div/div[2]/div[6]/ul/li[{index}]/div/div/div[1]/p/a'.format(index = i + 1))
            product_title = element.text
            print(product_title)
            element.click()
            sleep(delay)

            # identifying product id by form id path
            # https://www.bautura-online.ro/checkout/cart/add/uenc/aHR0cHM6Ly93d3cuYmF1dHVyYS1vbmxpbmUucm8vdGVhY2hlci1zLTcwLWNsLTY3OTEuaHRtbD9fX19TSUQ9VQ,,/product/65/form_key/KqsTys5VlkqAR6wy/
            # product id is between /product/ and /form_key/
            element = self.driver.find_element_by_xpath('//*[@id="product_addtocart_form"]')
            # getting the url
            url = element.get_attribute('action')
            # url.find returns the index of the first chr from the search string, in this case '/'
            # adding 9 (the length of the searched text) to get the index of the first digit in the index
            id_index_start = int(url.find("""/product/""")) + 9
            # getting the end of the slice, the first character that isn't in the id
            id_index_end = int(url.find("""/form_key/"""))
            # slicing the string
            product_id = url[id_index_start: id_index_end]
            sleep(delay)

            # getting current price
            element = self.driver.find_element_by_id('product-price-{product_id}'.format(product_id = product_id))
            price_text = element.text
            price = price_text[0: price_text.find(' RON')]
            print('Price is:', price)
            sleep(delay)

            # getting old price
            element = self.driver.find_element_by_id('old-price-{product_id}'.format(product_id = product_id))
            old_price_text = element.text
            old_price = old_price_text[0: price_text.find(' RON')]
            print('Price is:', old_price)
            sleep(delay)

            # getting the description
            # finding the outer div that contains the description
            element = self.driver.find_element_by_css_selector('div#pc-tab-description')
            # getting the text of the div
            description = element.get_attribute('innerHTML')
            # cleaning the description by removing <div> and </div>
            string_with_beginning_div = description[0:description.find('<p>')]
            description = description.replace(string_with_beginning_div, '')
            # rfind searched from the end of the string
            string_with_ending_div = description[(description.rfind('</p>') + 4): -1]
            description = description.replace(string_with_ending_div, '')
            print(description)
            sleep(delay)

            # getting attributes
            # finding attributes table
            element = self.driver.find_element_by_id('product-attribute-specs-table')
            attributes_html_string = element.get_attribute('innerHTML')

            sleep(delay)

            def extract_attributes_from_html(string, key):
                if string.find(key) != -1:
                    start_label_string = string.find(key)
                    start_concentration_string = string.find('<td class="data">', start_label_string) + 17
                    end_concentration_string = string.find('</td>', start_label_string)
                    return string[start_concentration_string:end_concentration_string]

            alcohol_concentration = extract_attributes_from_html(string = attributes_html_string,
                                                                 key = 'Concentrație Alcoolică')
            print(alcohol_concentration)
            brand = extract_attributes_from_html(string = attributes_html_string, key = 'Brand')
            print(brand)
            sleep(delay)

            # selecting the product image and printing the link
            element = self.driver.find_element_by_id('product-image-img')
            image_url = element.get_attribute('src')
            print(image_url)
            self.driver.execute_script("window.history.go(-1)")
            sleep(delay)

        try:
            self.driver.find_element_by_class_name('next.i-next').click()
        except ElementClickInterceptedException:
            sleep(delay)
            self.driver.find_element_by_class_name('next.i-next').click()
        except NoSuchElementException:
            break


class BBBot:
    def __init__(self, delay):
        # opening browser window
        self.driver = webdriver.Chrome()

        # maximizing window
        self.driver.maximize_window()

        # opening page in browser
        self.driver.get("https://www.bautura-online.ro")
        sleep(delay)

        # closing cookies pop-up
        self.driver.find_element_by_xpath('//*[@id="accept-all-cookies"]/span/span').click()
        sleep(delay)

        # closing underage pop-up
        self.driver.find_element_by_link_text('Da').click()
        sleep(delay)

        # going to Whisky category
        element = self.driver.find_element_by_css_selector('ul#nav>li:nth-of-type(2)>a')

        # clicking on the selected element (Whisky Category)
        self.driver.execute_script("arguments[0].click();", element)
        sleep(delay)

        # going back to main page
        self.driver.execute_script("window.history.go(-1)")
        sleep(delay)

        # and again to the whisky category to engage and get rid of email subscribe pop-up
        element = self.driver.find_element_by_css_selector('ul#nav>li:nth-of-type(2)>a')
        self.driver.execute_script("arguments[0].click();", element)

        # waiting for the pop-up to show
        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.presence_of_element_located((By.ID,
                                                   '__ra-modal-box-1')))

        # clicking of the closing X button
        element = self.driver.find_element_by_css_selector('div#__ra-modal-box-1>div>div>a')
        self.driver.execute_script("arguments[0].click();", element)
        sleep(delay)

        # --------- STARTING THE MAIN LOOP --------------
        main_category_loop(self, delay)
