from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

from hafta_2.test_saucedemo import TestSauceDemo


class Test_DemoClass:
    def setup_method(self):
        self.test_class = TestSauceDemo()

    def teardown_method(self):
        print("teardown")

    def test_valid_login(self):
        assert True == True
