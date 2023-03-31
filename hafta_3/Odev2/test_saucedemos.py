from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
from datetime import date
import pytest
import csv


class Test_SauceDemo:
    # driver = webdriver.Chrome(service=ChromeService(
    #     ChromeDriverManager().install()))
    # driver.maximize_window()

    # her testten önce calısır

    def setup_method(self):
        self.standard_user = "standard_user"
        self.locked_out_user = "locked_out_user"
        self.password = "secret_sauce"
        self.driver.get("https://www.saucedemo.com/")
        self.actions = ActionChains(self.driver)
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, "user-name")))
        self.username_input = self.driver.find_element(By.ID, "user-name")
        self.password_input = self.driver.find_element(By.ID, "password")
        self.login_btn = self.driver.find_element(By.ID, "login-button")
        self.folder_path = str(Path.cwd()) + \
            "\\hafta3\\Odev2\\" + str(date.today())
        Path(self.folder_path).mkdir(exist_ok=True)
    # her testten sonra çalısır

    def teardown_method(self):
        self.actions.release()

    def login(self):
        self.username_input.send_keys(self.standard_user)
        self.password_input.send_keys(self.password)

        self.login_btn.click()

    def get_data():
        reader = csv.reader("./data/invalid_login.csv")
        for data in reader:
            print(data)

    @pytest.mark.parametrize("password", [("12345678"), ("kullanici adi"), ("bir iki uc dort bes")])
    def test_blank_username_login(self, password):
        self.password_input.send_keys(password)
        self.login_btn.click()
        self.driver.save_screenshot(
            f"{self.folder_path}/blank-username-{password}.png")
        assert "Epic sadface: Username is required" == self.driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3').text

    @pytest.mark.parametrize("username", [("Emir"), ("Demir"), ("Cebir")])
    def test_blank_password_login(self, username):
        self.username_input.send_keys(username)
        self.login_btn.click()
        self.driver.save_screenshot(
            f"{self.folder_path}/blank-password-{username}.png")
        assert "Epic sadface: Password is required" == self.driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3').text

    def test_locked_out_user(self):
        self.actions.send_keys_to_element(
            self.username_input, self.locked_out_user)
        self.actions.send_keys_to_element(self.password_input, self.password)
        self.actions.perform()

        self.login_btn.click()
        self.driver.save_screenshot(f"{self.folder_path}/locked-out-user.png")
        assert "Epic sadface: Sorry, this user has been locked out." == self.driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3').text

    def test_x_icons(self):
        self.login_btn.click()

        self.driver.find_element(By.CLASS_NAME, "error-button").click()
        self.driver.save_screenshot(f"{self.folder_path}/x-icons.png")
        assert 0 == len(self.driver.find_elements(
            By.CLASS_NAME, "error_icon"))

    def test_valid_login(self):
        self.actions.send_keys_to_element(
            self.username_input, self.standard_user)
        self.actions.send_keys_to_element(self.password_input, self.password)
        self.actions.perform()

        self.login_btn.click()
        self.driver.save_screenshot(f"{self.folder_path}/valid-login.png")
        assert 6 == len(self.driver.find_elements(
            By.CLASS_NAME, "inventory_item"))

    @pytest.mark.parametrize("username,password", [("Emir", "123456"), ("123456", "Emir")])
    def test_invalid_login(self, username, password):
        self.actions.send_keys_to_element(
            self.username_input, username)
        self.actions.send_keys_to_element(self.password_input, password)
        self.actions.perform()

        self.login_btn.click()
        self.driver.save_screenshot(
            f"{self.folder_path}/invalid-login-{username}-{password}.png")
        assert "Epic sadface: Username and password do not match any user in this service" == self.driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3').text

    def test_total_amount(self):
        self.login()

        prices = self.driver.find_elements(
            By.CLASS_NAME, "inventory_item_price")
        total = 0.0

        for price in prices:
            total += float(price.text.removeprefix("$"))
        self.driver.save_screenshot(f"{self.folder_path}/total-amount.png")

        assert 129.94 == total

    def test_menu_items(self):
        self.login()

        assert 4 == len(self.driver.find_elements(By.CLASS_NAME, "menu-item"))

    def test_shopping_cart_badge(self):
        self.login()
        self.driver.find_element(
            By.ID, "add-to-cart-sauce-labs-backpack").click()
        self.driver.save_screenshot(
            f"{self.folder_path}/shopping-cart-badge.png")
        assert "1" == self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_badge").text

    @pytest.mark.parametrize("bir,iki,uc,dort,bes", [("param1", "param2", "param3", "param4", "param5")])
    def test_parametrize(self, bir, iki, uc, dort, bes):
        l = []
        l.append(bir)
        l.append(iki)
        l.append(uc)
        l.append(dort)
        l.append(bes)
        print(l)
        print()

    def test_wrong_image(self):
        self.username_input.send_keys("problem_user")
        self.password_input.send_keys(self.password)
        self.login_btn.click()

        sleep(1)
        img1 = self.driver.find_element(
            By.CSS_SELECTOR, '[alt="Sauce Labs Backpack"]')
        img1_src = img1.get_attribute("src")
        img1.click()
        sleep(1)
        img2_src = self.driver.find_element(
            By.CSS_SELECTOR, '[alt="Sauce Labs Fleece Jacket"]').get_attribute("src")

        assert not img1_src == img2_src

    def test_all_images(self):
        self.username_input.send_keys("problem_user")
        self.password_input.send_keys(self.password)
        self.login_btn.click()

        sleep(1)
        a_tags_with_img = self.driver.find_elements(By.XPATH, '//a[img]')

        img_src_tuples = []

        for i in range(len(a_tags_with_img)):
            a_tag = a_tags_with_img[0]
            img_tag = a_tag.find_element(By.TAG_NAME, 'img')
            img_src = img_tag.get_attribute('src')

            img_tag.click()

            next_img_tag = self.driver.find_element(By.TAG_NAME, 'img')
            next_img_src = next_img_tag.get_attribute('src')

            img_src_tuples.append((img_src, next_img_src))

            self.driver.back()

            a_tags_with_img = self.driver.find_elements(
                By.XPATH, '//a[img]')[i+1:]

        for src in img_src_tuples:
            assert not src[0] == src[1]

    def test_buttons(self):
        self.login()

        assert 6 == len(self.driver.find_elements(By.CLASS_NAME, "btn"))
