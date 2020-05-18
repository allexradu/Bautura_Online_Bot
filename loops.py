from time import sleep
import threading
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import datetime
import threading

import extra_functions
import ranges
import excel

time = datetime.datetime.now()

threads = []


def main_category_loop(self, delay):
    """This loop function goes trough the MAIN product categories"""
    for main_category_index in range(2, 9):
        # finding the main category in the loop at the selected index
        try:
            elem = self.driver.find_element_by_css_selector(extra_functions.main_category_css_path(main_category_index))
            excel.product_data.main_category = elem.text
            print(excel.product_data.main_category)
            # clicking on main category
            self.driver.execute_script("arguments[0].click();", elem)

            sleep(delay)

            # starting the loops of sub-categories
            sub_category_loop(self, delay)
            print('main category index is:', main_category_index)
        except NoSuchElementException:
            excel.product_data.main_category = 'n/a'


def sub_category_loop(self, delay):
    """This function loops trough the available sub-categories"""
    global threads
    sleep(delay)
    loop_size = ranges.find_sub_category_range_size(self)

    sleep(delay)

    print('sub category loop length: ', loop_size)
    # If the category has no sub-categories the loop_size is zero, so we check for that
    if loop_size != 0:
        for i in range(loop_size):
            print('sub category index is: ', i)
            # clicking on the sub-category at the index
            try:
                # finding the sub-category at the index by xpath
                element = self.driver.find_element_by_xpath(extra_functions.sub_category_xpath(i))
                excel.product_data.sub_category = element.text
                print('sub category: ', element.text)
                # clicking on the element
                element.click()
                sleep(delay)

                # looping trough product pages at the specified category
                main_thread = threading.Thread(target = product_page_loop(self, delay))
                main_thread.start()
                threads.append(main_thread)

            except NoSuchElementException:
                print('no element sub-category: ', i)
                print('XPATH: ', extra_functions.sub_category_xpath(i))
                excel.product_data.sub_category = 'n/a'

            except ElementClickInterceptedException:
                excel.product_data.sub_category = 'n/a'
                print('element interrupted')


def product_page_loop(self, delay):
    """This function loops over the product pages in a category or sub-category"""
    index = 1
    url = ''

    for thread in threads:
        thread.join()

    try:
        # finding the class that has the "»", the url to the last page from the page selector
        element = self.driver.find_element_by_class_name('last-page')
        inner_html = element.get_attribute('innerHTML')

        # the resulting HTML contains the fallowing code:
        # <a href="https://www.bautura-online.ro/{main_category}.html?p={the_last_page}">
        # extracting the last page number from the URL
        extra_functions.last_page = int(inner_html[(inner_html.find('p=') + 2):inner_html.find('">')])
        # extracting the URL without the page number
        url_raw = inner_html[(inner_html.find('href="') + 6): (inner_html.find('p=') + 2)]
        # replacing the &amp; with & in the sub-category links
        url = url_raw.replace('&amp;', '&') if url_raw.find('&') != 1 else url_raw

    except NoSuchElementException:
        # if there is no "»" (last page in the page selector) on the page
        # that means there fist page is the last page in the category or sub-category
        extra_functions.last_page = 1
        print('last page indicator not detected')

    while index <= extra_functions.last_page:

        for i in range(ranges.find_product_range_size(self) - 1):
            global time
            # for i in range(1):  # FOR TESTING ONLY, REPLACE WITH THE LINE ABOVE!!!
            # clicking on the product at hte index
            clicking_on_product(self, i, delay)
            # getting the product id
            getting_product_id(self, delay)
            # getting the price both the current and slashed price
            getting_price(self, delay)
            # getting the product description
            getting_description(self, delay)
            # getting the product attributes
            getting_attributes(self, delay)
            # getting the product image URL
            getting_product_image_url(self, delay)

            # move the browser back to current product page

            def save_excel():
                global time
                time_difference = datetime.datetime.now() - time
                excel.product_data.time_difference = '{} s'.format(str(time_difference))
                time = datetime.datetime.now()
                excel.product_data.time = time.strftime("%d-%m-%Y %H:%M:%S")
                excel.save_product_to_excel()
                excel.work_sheet_index += 1

            excel_thread = threading.Thread(target = save_excel)
            excel_thread.start()
            threads.append(excel_thread)

            self.driver.execute_script("window.history.go(-1)")
            sleep(delay)

        # if the first page is also the last page in the category or sub-category
        if extra_functions.last_page == 1:
            print('first page is last page, going back 1')
            self.driver.execute_script("window.history.go(-1)")
            sleep(10)
            break

        # if we have more than one page and where are not on the last page
        if index != extra_functions.last_page:
            print('current product page url + {url}{index}'.format(index = index, url = url))
            print('next product page url + {url}{index}'.format(index = index + 1, url = url))
            sleep(delay)
            # going to the next page in the category or sub-category
            self.driver.get(url + '{index}'.format(index = index + 1))
            sleep(delay)
            index += 1

        # if we are on the last page in the category that isn't also the first page in the category or sub-category
        else:
            print('current product page url {url}{index}'.format(index = index, url = url))
            # going back as many pages as we traveled to the main category
            for i in range(index):
                print('going back {index} time(s)'.format(index = i + 1))
                print('current product page url {url}{index}'.format(index = index, url = url))
                self.driver.execute_script("window.history.go(-1)")

            sleep(10)
            break


def clicking_on_product(self, i, delay):
    # getting the product element in the index, getting the title and clicking on the fist product
    try:
        element = self.driver.find_element_by_xpath(extra_functions.product_xpath(i + 1))
        excel.product_data.product_title = element.text
        print("Product title:", excel.product_data.product_title)
        element.click()
        sleep(delay)
    except NoSuchElementException:
        excel.product_data.product_title = 'n/a'
        print('Product URL NOT FOUND')

    except ElementClickInterceptedException:
        excel.product_data.product_title = 'n/a'
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
        excel.product_data.product_id = url[id_index_start: id_index_end]
        sleep(delay)
        return excel.product_data.product_id

    except NoSuchElementException:
        print('no product id')
        excel.product_data.product_id = 'n/a'


def getting_price(self, delay):
    try:
        # getting current price
        element = self.driver.find_element_by_id(
            'product-price-{product_id}'.format(product_id = getting_product_id(self, delay)))
        excel.product_data.price_text = element.text
        price = excel.product_data.price_text[0: excel.product_data.price_text.find(' RON')]
        print('Price is:', price)
        sleep(delay)
    except NoSuchElementException:
        print('No price found')
        excel.product_data.price_text = 'n/a'

    try:
        # getting old price
        element = self.driver.find_element_by_id(
            'old-price-{product_id}'.format(product_id = getting_product_id(self, delay)))
        excel.product_data.old_price_text = element.text
        old_price = excel.product_data.old_price_text[
                    0: excel.product_data.price_text.find(' RON')]
        print('Old price is:', old_price)
        sleep(delay)
    except NoSuchElementException:
        print('No old price found')
        excel.product_data.old_price_text = 'n/a'


def getting_description(self, delay):
    try:
        sleep(delay)
        # getting the description
        # finding the outer div that contains the description
        element = self.driver.find_element_by_css_selector('div#pc-tab-description>div')
        sleep(delay)
        # getting the text of the div
        excel.product_data.description = element.get_attribute('innerHTML')
        print(excel.product_data.description)
        sleep(delay)
    except NoSuchElementException:
        excel.product_data.description = 'n/a'
        print('No description found')


def getting_attributes(self, delay):
    try:
        # getting attributes
        # finding attributes table
        element = self.driver.find_element_by_id('product-attribute-specs-table')
        attributes_html_string = element.get_attribute('innerHTML')

        sleep(delay)
        # getting the product attribute
        excel.product_data.alcohol_concentration = extra_functions.extract_attributes_from_html(
            string = attributes_html_string,
            key = 'Concentrație Alcoolică')
        # print(excel.product_data.alcohol_concentration)
        excel.product_data.brand = extra_functions.extract_attributes_from_html(string = attributes_html_string,
                                                                                key = 'Brand')
        print(excel.product_data.brand)
        sleep(delay)
    except NoSuchElementException:
        print('Mo product attributes found')
        excel.product_data.alcohol_concentration = 'n/a'
        excel.product_data.brand = 'n/a'


def getting_product_image_url(self, delay):
    try:
        # selecting the product image and printing the link
        element = self.driver.find_element_by_id('product-image-img')
        excel.product_data.image_url = element.get_attribute('src')
        sleep(delay)
        print(excel.product_data.image_url)

    except NoSuchElementException:
        print('No product image found')
        excel.product_data.image_url = 'n/a'
