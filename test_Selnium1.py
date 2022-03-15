####Importing all the libraries
import pytest
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service impvenort Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import yaml
import time

links=[]
dfs=[]
config={}

with open("test_data.yml", "r") as f:
    try:
        config = yaml.load(f, Loader=yaml.FullLoader)
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.maximize_window()
        driver.get(config['search']['page'])
        links = [elem.get_attribute("href") for elem in driver.find_elements(by=By.TAG_NAME, value=config['search']['tag'])]
        expected_url_count = config['search']['urlcount']
    except yaml.YAMLError as exc:
        print(exc)

##Count the number of Links in the web application
def test_count():
    print("expected_url_count is", expected_url_count)
    ##assertEqual
    assert expected_url_count == len(links)

###Test case to check there are no dead links/urls
def test_active_urls():
    for link in links:
        try:
            if link in (None, 'javascript:print();'):
                print("Invalid Link")
            else:
                print(link)
                req = requests.get(link)
                print(req.status_code)
                assert req.status_code == requests.codes['ok']
        except Exception as ex:
            print(f'Something went wrong: {ex}')
            pytest.fail({ex})

##Test case to validate all expected Urls are present in Web Page.
def test_url_data_validation():
    try:
        dfs = pd.read_excel("urls.xls")
    except Exception as exc:
        print(exc)
    try:
        check = all(item in dfs for item in links)
        print(check)
    except Exception as e:
        print("exception occurred",e)
    assert check

driver.close()
