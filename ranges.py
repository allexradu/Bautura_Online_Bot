from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import extra_functions


def find_sub_category_range_size(self):
    range_size = 1

    while True:
        try:
            elem = self.driver.find_element_by_xpath(extra_functions.sub_category_xpath(range_size))
        except NoSuchElementException:
            if range_size == 1:
                range_size = 0
                break
            else:
                break
        else:
            print(elem.text)
            range_size += 1
            print(range_size)

    return range_size


def find_product_range_size(self):
    range_size = 1

    while True:
        try:
            elem = self.driver.find_element_by_xpath(extra_functions.product_xpath(range_size))
            print(elem.text)
            range_size += 1
        except NoSuchElementException:
            break

    return range_size
