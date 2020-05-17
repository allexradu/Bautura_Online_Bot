from time import sleep

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import loops


class BBBot:
    def __init__(self, delay):
        # Uncomment the lines bellow to run Chrome Headless
        # self.display = Display(visible = 0, size = (1920, 1080))
        # self.display.start()

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("disable-gpu")
        chrome_options.add_argument("window-size=1400,2100")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

        # opening browser window
        # self.driver = webdriver.Chrome()

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

        # going back to main page to trigger pop-up
        self.driver.execute_script("window.history.go(-1)")
        sleep(delay)

        # and again to the whisky category to engage and get rid of email subscribe pop-up
        element = self.driver.find_element_by_css_selector('ul#nav>li:nth-of-type(2)>a')
        self.driver.execute_script("arguments[0].click();", element)

        # waiting for the pop-up to show
        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.presence_of_element_located((By.ID,
                                                   '__ra-modal-box-1')))

        # clicking of the closing X button to close the pop-up
        element = self.driver.find_element_by_css_selector('div#__ra-modal-box-1>div>div>a')
        self.driver.execute_script("arguments[0].click();", element)
        sleep(delay)

        # --------- STARTING THE MAIN LOOP --------------
        loops.main_category_loop(self, delay)
