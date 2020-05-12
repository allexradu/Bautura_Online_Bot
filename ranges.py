from selenium.common.exceptions import NoSuchElementException

import extra_functions


def find_sub_category_range_size(self):
    range_size = 1

    try:
        extra_functions.narrow_list_html = self.driver.find_element_by_id('narrow-by-list').get_attribute('innerHTML')
    except NoSuchElementException:
        print('Not found narrow_by_list')

    while True:
        try:
            elem = self.driver.find_element_by_xpath(extra_functions.sub_category_xpath(range_size))
        except NoSuchElementException:
            print("NO XPATH FOUND: ", extra_functions.sub_category_xpath(range_size))
            print('No element in find subcategory. Index is:', range_size)
            if range_size == 1:
                range_size = 0
                break
            else:
                # range_size -= 1
                break
        else:

            if extra_functions.narrow_list_html.find('<dt>Categorie</dt>') != -1:
                print('Found Category: ' + elem.text + 'Index is:' + str(range_size))
                range_size += 1
            else:
                range_size = 0
    return range_size


def find_product_range_size(self):
    range_size = 1

    while True:
        try:
            elem = self.driver.find_element_by_xpath(extra_functions.product_xpath(range_size))

        except NoSuchElementException:
            print()
            print('No element found in Main Category with Index: ', range_size)
            break
        else:
            print(elem.text)
            range_size += 1

    return range_size
