from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from pathlib import Path
from datetime import date
import pytest
import csv
import constants


class Test_SauceDemo:
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()))
    driver.maximize_window()

    # her testten önce calısır
    def setup_method(self):
        self.standard_user = constants.STANDARD_USER
        self.locked_out_user = constants.LOCKED_OUT_USER
        self.password = constants.PASSWORD
        self.driver.get(constants.URL)
        self.actions = ActionChains(self.driver)
        WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, constants.USERNAME_ID)))
        self.username_input = self.driver.find_element(
            By.ID, constants.USERNAME_ID)
        self.password_input = self.driver.find_element(
            By.ID, constants.PASSWORD_ID)
        self.login_btn = self.driver.find_element(
            By.ID, constants.LOGIN_BTN_ID)
        self.folder_path = str(Path.cwd()) + \
            "\\hafta_4\\Odev2\\" + str(date.today())
        Path(self.folder_path).mkdir(exist_ok=True)
    # her testten sonra çalısır

    def teardown_method(self):
        self.actions.release()

    def login(self):
        self.username_input.send_keys(constants.STANDARD_USER)
        self.password_input.send_keys(constants.PASSWORD)

        self.login_btn.click()

    def reset_app_state(self):
        self.driver.find_element(By.ID, constants.MENU_BTN_ID).click()
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(
            (By.ID, constants.RESET_APP_STATE_BTN_ID)))
        self.driver.find_element(
            By.ID, constants.RESET_APP_STATE_BTN_ID).click()

    def wait(self, element: tuple, max_time: int = 5):
        WebDriverWait(self.driver, max_time).until(
            expected_conditions.visibility_of_element_located(element))

    def get_data(selection: str):
        with open(r"hafta_4\Odev2\data\login_credentials.csv", "r", newline='') as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            data = []
            match selection:
                case "username":
                    for row in reader:
                        data.append(row["username"])
                case "password":
                    for row in reader:
                        data.append(row["password"])
                case "both":
                    for row in reader:
                        data.append((row["username"], row["password"]))
        return data

    def get_checkout_inputs(self):
        return (self.driver.find_element(By.ID, constants.CHECK_OUT_FIRSTNAME_ID), self.driver.find_element(By.ID, constants.CHECK_OUT_LASTNAME_ID), self.driver.find_element(By.ID, constants.CHECK_OUT_POSTALCODE_ID))

    @pytest.mark.parametrize("password", get_data("password"))
    def test_blank_username_login(self, password):
        self.password_input.send_keys(password)
        self.login_btn.click()
        self.driver.save_screenshot(
            f"{self.folder_path}/blank-username-{password}.png")
        assert constants.BLANK_USERNAME_MESSAGE == self.driver.find_element(
            By.XPATH, constants.ERROR_MESSAGE_XPATH).text

    @pytest.mark.parametrize("username", get_data("username"))
    def test_blank_password_login(self, username):
        self.username_input.send_keys(username)
        self.login_btn.click()
        self.driver.save_screenshot(
            f"{self.folder_path}/blank-password-{username}.png")
        assert constants.BLANK_PASSWORD_MESSAGE == self.driver.find_element(
            By.XPATH, constants.ERROR_MESSAGE_XPATH).text

    def test_locked_out_user(self):
        self.actions.send_keys_to_element(
            self.username_input, self.locked_out_user)
        self.actions.send_keys_to_element(self.password_input, self.password)
        self.actions.perform()

        self.login_btn.click()
        self.driver.save_screenshot(f"{self.folder_path}/locked-out-user.png")
        assert constants.LOCKED_OUT_USER_MESSAGE == self.driver.find_element(
            By.XPATH, constants.ERROR_MESSAGE_XPATH).text

    def test_x_icons(self):
        self.login_btn.click()

        self.driver.find_element(By.CLASS_NAME, "error-button").click()
        self.driver.save_screenshot(f"{self.folder_path}/x-icons.png")

        assert 0 == len(self.driver.find_elements(
            By.CLASS_NAME, constants.ERROR_ICON_CLASS))

    def test_valid_login(self):
        self.actions.send_keys_to_element(
            self.username_input, self.standard_user)
        self.actions.send_keys_to_element(self.password_input, self.password)
        self.actions.perform()

        self.login_btn.click()
        self.driver.save_screenshot(f"{self.folder_path}/valid-login.png")
        assert 6 == len(self.driver.find_elements(
            By.CLASS_NAME, constants.INVENTORY_ITEM_CLASS))

    @pytest.mark.parametrize("username,password", get_data("both"))
    def test_invalid_login(self, username, password):
        self.actions.send_keys_to_element(
            self.username_input, username)
        self.actions.send_keys_to_element(self.password_input, password)
        self.actions.perform()

        self.login_btn.click()
        self.driver.save_screenshot(
            f"{self.folder_path}/invalid-login-{username}-{password}.png")
        assert constants.INVALID_LOGIN_MESSAGE == self.driver.find_element(
            By.XPATH, constants.ERROR_MESSAGE_XPATH).text

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

    @pytest.mark.parametrize("sort_by", [("az"), ("za")])
    def test_sorting_by_name(self, sort_by: str):
        self.login()

        match sort_by:
            case "az":
                Select(self.driver.find_element(By.CLASS_NAME,
                       "product_sort_container")).select_by_index(0)
                first_item_name = self.driver.find_element(
                    By.XPATH, constants.FIRST_ITEM_XPATH).text

                assert first_item_name == "Sauce Labs Backpack"
            case "za":
                Select(self.driver.find_element(By.CLASS_NAME,
                       "product_sort_container")).select_by_index(1)
                first_item_name = self.driver.find_element(
                    By.XPATH, constants.FIRST_ITEM_XPATH).text

                assert first_item_name == "Test.allTheThings() T-Shirt (Red)"

    @pytest.mark.parametrize("sort_by", [("lh"), ("hl")])
    def test_sorting_by_price(self, sort_by: str):
        self.login()

        match sort_by:
            case "lh":
                Select(self.driver.find_element(By.CLASS_NAME,
                       "product_sort_container")).select_by_index(2)
                first_item_price = self.driver.find_element(
                    By.XPATH, constants.FIRST_ITEM_PRICE_XPATH).text

                assert first_item_price == "$7.99"
            case "hl":
                Select(self.driver.find_element(By.CLASS_NAME,
                       "product_sort_container")).select_by_index(3)
                first_item_price = self.driver.find_element(
                    By.XPATH, constants.FIRST_ITEM_PRICE_XPATH).text

                assert first_item_price == "$49.99"

    @pytest.mark.parametrize("num_of_btns_to_click", [1, 3])
    def test_shopping_cart_badge(self, num_of_btns_to_click: int):
        self.login()

        self.wait((By.CLASS_NAME, constants.INVENTORY_BUTTON_CLASS))

        btns = self.driver.find_elements(By.CLASS_NAME, constants.INVENTORY_BUTTON_CLASS)

        for i in range(num_of_btns_to_click):
            btns[i].click()

        badge_number_count = self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_badge").text

        self.driver.save_screenshot(
            f"{self.folder_path}/shopping-cart-badge.png")
        self.driver.refresh()

        btns = self.driver.find_elements(By.CLASS_NAME, constants.INVENTORY_BUTTON_CLASS)
        for i in range(num_of_btns_to_click):
            btns[i].click()

        assert str(num_of_btns_to_click) == badge_number_count

    def test_empty_checkout_info(self):
        self.login()

        self.driver.find_element(
            By.CLASS_NAME, constants.SHOPPING_CART_CLASS).click()
        self.driver.find_element(By.ID, constants.CHECKOUT_BTN_ID).click()
        self.driver.find_element(By.ID, constants.CONTINUE_BTN_ID).click()

        self.driver.save_screenshot(
            f"{self.folder_path}/empty-checkout-info.png")

        assert 3 == len(self.driver.find_elements(
            By.CLASS_NAME, constants.ERROR_ICON_CLASS))

    def test_checkout_empty_firstname(self):
        self.login()

        self.driver.find_element(
            By.CLASS_NAME, constants.SHOPPING_CART_CLASS).click()
        self.driver.find_element(By.ID, constants.CHECKOUT_BTN_ID).click()
        _, last_name, postal_code = self.get_checkout_inputs()
        last_name.send_keys("soyisim")
        postal_code.send_keys("posta-kodu-12345")

        self.driver.find_element(By.ID, constants.CONTINUE_BTN_ID).click()

        self.driver.save_screenshot(
            f"{self.folder_path}/checkout-empty-firstname.png")

        assert constants.FIRST_NAME_MESSAGE == self.driver.find_element(
            By.XPATH, constants.CHECKOUT_ERROR_MESSAGE_XPATH).text

    def test_checkout_empty_lastname(self):
        self.login()

        self.driver.find_element(
            By.CLASS_NAME, constants.SHOPPING_CART_CLASS).click()
        self.driver.find_element(By.ID, constants.CHECKOUT_BTN_ID).click()
        first_name, _, postal_code = self.get_checkout_inputs()
        first_name.send_keys("emir")
        postal_code.send_keys("posta-kodu-12345")

        self.driver.find_element(By.ID, constants.CONTINUE_BTN_ID).click()

        self.driver.save_screenshot(
            f"{self.folder_path}/checkout-empty-lastname.png")

        assert constants.LASTNAME_MESSAGE == self.driver.find_element(
            By.XPATH, constants.CHECKOUT_ERROR_MESSAGE_XPATH).text

    def test_checkout_empty_postal_code(self):
        self.login()

        self.driver.find_element(
            By.CLASS_NAME, constants.SHOPPING_CART_CLASS).click()
        self.driver.find_element(By.ID, constants.CHECKOUT_BTN_ID).click()
        first_name, last_name, _ = self.get_checkout_inputs()
        first_name.send_keys("emir")
        last_name.send_keys("soyisim")

        self.driver.find_element(By.ID, constants.CONTINUE_BTN_ID).click()

        self.driver.save_screenshot(
            f"{self.folder_path}/checkout-empty-postalcode.png")

        assert constants.POSTAL_CODE_MESSAGE == self.driver.find_element(
            By.XPATH, constants.CHECKOUT_ERROR_MESSAGE_XPATH).text

    def test_valid_checkout_info(self):
        self.login()

        self.driver.find_element(
            By.CLASS_NAME, constants.SHOPPING_CART_CLASS).click()
        self.driver.find_element(By.ID, constants.CHECKOUT_BTN_ID).click()
        first_name, last_name, postal_code = self.get_checkout_inputs()
        first_name.send_keys("emir")
        last_name.send_keys("soyisim")
        postal_code.send_keys("posta-kodu-12345")

        self.driver.find_element(By.ID, constants.CONTINUE_BTN_ID).click()

        self.driver.save_screenshot(
            f"{self.folder_path}/valid-checkout-info.png")

        assert "Checkout: Overview" == self.driver.find_element(
            By.CLASS_NAME, "title").text

    @pytest.mark.parametrize("num_of_items_to_add", [1, 3, 5])
    def test_cart_item(self, num_of_items_to_add: int):
        self.login()

        items = self.driver.find_elements(By.CLASS_NAME, constants.INVENTORY_BUTTON_CLASS)

        for i in range(num_of_items_to_add):
            items[i].click()

        self.driver.find_element(
            By.CLASS_NAME, constants.SHOPPING_CART_CLASS).click()

        cart_items = self.driver.find_elements(By.CLASS_NAME, constants.CART_ITEM_CLASS)

        self.driver.save_screenshot(
            f"{self.folder_path}/cart-item.png")

        self.driver.back()

        items = self.driver.find_elements(By.CLASS_NAME, constants.INVENTORY_BUTTON_CLASS)

        for i in range(num_of_items_to_add):
            items[i].click()

        assert num_of_items_to_add == len(cart_items)

    def test_number_of_social_links(self):
        self.login()

        assert 3 == len(self.driver.find_element(
            By.CLASS_NAME, "social").find_elements(By.TAG_NAME, "li"))

    def test_price_after_tax(self):
        self.login()

        items = self.driver.find_elements(By.CLASS_NAME, constants.INVENTORY_BUTTON_CLASS)

        for item in items:
            item.click()

        self.driver.find_element(
            By.CLASS_NAME, constants.SHOPPING_CART_CLASS).click()
        self.driver.find_element(By.ID, constants.CHECKOUT_BTN_ID).click()
        first_name, last_name, postal_code = self.get_checkout_inputs()
        first_name.send_keys("emir")
        last_name.send_keys("soyisim")
        postal_code.send_keys("posta-kodu-12345")

        self.driver.find_element(By.ID, constants.CONTINUE_BTN_ID).click()

        self.driver.save_screenshot(
            f"{self.folder_path}/price-after-tax.png")

        total = self.driver.find_element(
            By.CLASS_NAME, "summary_total_label").text.removeprefix("Total: $")

        assert "140.34" == total

    def test_logout(self):
        self.login()
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()

        WebDriverWait(self.driver, 3).until(
            expected_conditions.element_to_be_clickable((By.ID, "logout_sidebar_link")))

        self.driver.find_element(By.ID, "logout_sidebar_link").click()

        self.driver.save_screenshot(
            f"{self.folder_path}/logout.png")

        assert self.driver.current_url == "https://www.saucedemo.com/"

    def test_inventory_buttons(self):
        self.login()

        assert 6 == len(self.driver.find_elements(
            By.CLASS_NAME, constants.INVENTORY_BUTTON_CLASS))
