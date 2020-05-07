from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from selenium.webdriver.common.keys import Keys


class BBBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.bautura-online.ro")
        self.driver.find_element_by_xpath('//*[@id="accept-all-cookies"]/span/span').click()
        self.driver.find_element_by_link_text('Da').click()
        sleep(1)
        element = self.driver.find_element_by_css_selector('ul#nav>li:nth-of-type(2)>a')
        self.driver.execute_script("arguments[0].click();", element)
        sleep(1)
        self.driver.execute_script("window.history.go(-1)")
        sleep(1)
        element = self.driver.find_element_by_css_selector('ul#nav>li:nth-of-type(2)>a')
        self.driver.execute_script("arguments[0].click();", element)

        element = self.driver.find_element_by_css_selector('div#__ra-modal-box-1>div>div>a')
        self.driver.execute_script("arguments[0].click();", element)

        # elem = self.driver.find_element_by_id('__ra-ldsd-email')
        # elem.send_keys("a@b.com")
        # elem.send_keys(Keys.RETURN)

        # opens the link in a new tab
        # link_object = self.driver.find_element_by_xpath('//*[@id="nav"]/li[2]/a')
        # url = link_object.get_attribute('href')
        # self.driver.execute_script("window.open('{url}');".format(url = url))
        # base_window = self.driver.window_handles[0]

        # self.driver.switch_to.window(self.driver.window_handles[-1])
        #
        # WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.ID, "CloseLink"))).click()

        # self.driver.find_element_by_xpath('//*[@id="__ra-modal-box-1"]/div[1]/div/a[1]')
