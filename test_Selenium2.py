###Importing all the libraries
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import yaml


####Test case for Search valid text
def test_search_basic():
    with open("test_data.yml", "r") as f:
        try:
            config = yaml.load(f, Loader=yaml.FullLoader)
            s = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=s)
            driver.get(config['search']['page'])
            driver.maximize_window()
            print(driver.title)
            driver.find_element(by=By.NAME, value=config['search']['search_pad']).send_keys(config['search']['search_text'])
            time.sleep(2)
            ##Click on search button
            driver.find_element(by=By.XPATH, value=config['search']['search_in_xpath']).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, config['search']['search_text'])))
        except TimeoutException:
            print("Element was not clickable in Time")
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, config['search']['search_result_1'])))
        except TimeoutException:
            print("Element was not clickable in Time")
        try:
            driver.find_element(by=By.XPATH, value=config['search']['search_result_1']).click()
        except:
            print("Expected Search Result not found")
        try:
            WebDriverWait(driver, 20).until(EC.url_to_be(config['search']['result_url']))
            print(driver.current_url)
            print("Desired url was rendered with in allocated time")
            assert driver.current_url == config['search']['result_url']
        except TimeoutException:
            print("Current URL is **********", driver.current_url)
            print("Desired url was not rendered with in allocated time", driver.current_url)

        except yaml.YAMLError as exc:
            print(exc)
        driver.close()


