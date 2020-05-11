from time import sleep
import extra_functions
import ranges
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException


def main_category_loop(self, delay):
    for main_category_index in range(2, 9):
        # pressing the main category in the loop
        elem = self.driver.find_element_by_css_selector(
            'ul#nav>li:nth-of-type({main_category_index})>a'.format(main_category_index = main_category_index))
        main_category = elem.text
        print(main_category)
        self.driver.execute_script("arguments[0].click();", elem)

        sleep(delay)

        sub_category_loop(self, ranges.find_sub_category_range_size(self), delay)


def sub_category_loop(self, loop_size, delay):
    if loop_size != 0:
        print('sub cat', loop_size)
        for i in range(loop_size):
            # clicking on the fist sub-category
            # //*[@id="narrow-by-list"]/dd[1]/ol/li[THIS IS THE PARAMETER THAT CHANGES]/a
            try:
                element = self.driver.find_element_by_xpath(extra_functions.sub_category_xpath(i))
                sub_category = element.text
                print(sub_category)
                element.click()
                sleep(delay)
                product_page_loop(self, delay)

            except NoSuchElementException:
                print('no element')
            except ElementClickInterceptedException:
                print('element interrupted')


        else:
            product_page_loop(self, delay)


def product_page_loop(self, delay):
    element = self.driver.find_element_by_class_name('last-page')
    inner_html = element.get_attribute('innerHTML')
    last_page = int(inner_html[(inner_html.find('p=') + 2):inner_html.find('">')])
    url = inner_html[(inner_html.find('href="') + 6): inner_html.find('p=')]
    index = 1

    while index <= last_page:
        for i in range(ranges.find_product_range_size(self) - 1):
            clicking_on_product(self, i, delay)
            getting_product_id(self, delay)
            getting_price(self, delay)
            getting_description(self, delay)
            getting_attributes(self, delay)
            getting_product_image_url(self, delay)

            self.driver.execute_script("window.history.go(-1)")
            sleep(delay)

        if index != last_page:
            self.driver.get(url + '?p={index}'.format(index = index + 1))

    self.driver.execute_script("window.history.go(-1)")

    # element = self.driver.find_element_by_class_name('last-page')
    # html_string = element.get_attribute('innerHTML')
    # last_page = int(html_string[(html_string.find('?p=') + 3): html_string.find('"><span>')])

    # if index != last_page:
    #     self.driver.get(navigation_url + '?p={index}'.format(index = index))
    # else:
    #     if has_sub_category:
    #         self.driver.get(main_category_url)
    #         break
    #     else:
    #         break


def clicking_on_product(self, i, delay):
    # getting the first product element, getting the title and clicking on the fist product
    # /html/body/main/div/div/div/div[2]/div[6]/ul/li[THIS IS THE PARAMETER THAT CHANGES]/div/div/div[1]/p/a
    try:
        element = self.driver.find_element_by_xpath(
            '/html/body/main/div/div/div/div[2]/div[6]/ul/li[{index}]/div/div/div[1]/p/a'.format(index = i + 1))
        product_title = element.text
        print(product_title)
        element.click()
        sleep(delay)

    except ElementClickInterceptedException:
        sleep(2)
        print('Element Interrupted')


def getting_product_id(self, delay):
    try:
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
        return product_id
    except NoSuchElementException:
        print('no product id')


def getting_price(self, delay):
    price_text = ''
    try:
        # getting current price
        element = self.driver.find_element_by_id(
            'product-price-{product_id}'.format(product_id = getting_product_id(self, delay)))
        price_text = element.text
        price = price_text[0: price_text.find(' RON')]
        print('Price is:', price)
        sleep(delay)
    except NoSuchElementException:
        print('no price')

    try:
        # getting old price
        element = self.driver.find_element_by_id(
            'old-price-{product_id}'.format(product_id = getting_product_id(self, delay)))
        old_price_text = element.text
        old_price = old_price_text[0: price_text.find(' RON')]
        print('Price is:', old_price)
        sleep(delay)
    except NoSuchElementException:
        print('no old price')


def getting_description(self, delay):
    try:
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
        # print(description)
        sleep(delay)
    except NoSuchElementException:
        print('no description')


def getting_attributes(self, delay):
    try:
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
    except NoSuchElementException:
        print('no attributes')


def getting_product_image_url(self, delay):
    try:
        # selecting the product image and printing the link
        element = self.driver.find_element_by_id('product-image-img')
        image_url = element.get_attribute('src')
        print(image_url)

    except NoSuchElementException:
        print('no image')
