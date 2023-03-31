from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from colorama import Fore, init

class SauceDemo:

    def __init__(self):
        init(autoreset=True)
        self.url = "https://www.saucedemo.com/"
        self.standard_user = "standard_user"
        self.locked_out_user = "locked_out_user"
        self.password = "secret_sauce"
        self.driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()))
        self.already_opened = False
        self.username_input = None
        self.password_input = None
        self.login_btn = None
        self.error_message = ""
        self.actions = ActionChains(self.driver)
        self.open_url()

    def avaliable_commands(self):
        # Kullanıcının kullanabileceği komutların listesi
        print()
        print(Fore.LIGHTWHITE_EX + "Kullanabilecek olduğunuz komutlar.")
        print()
        print(f"Bütün Testler için {Fore.BLUE + 'All': >35}")
        print(
            f"Geçerli Kullanıcı Testi için {Fore.LIGHTCYAN_EX + 'valid_login' : >33}")
        print(
            f"Boş Kullanıcı Adı ve Şifre Testi için {Fore.LIGHTRED_EX + 'invalid_login' : >26}")
        print(
            f"Hatalı Şifre Testi için {Fore.GREEN + 'invalid_password' : >43}")
        print(
            f"Giriş yapması yasak olan Kullanıcı Testi için {Fore.LIGHTYELLOW_EX + 'locked_out_user'}")
        print(
            f"X ikonları Testi için {Fore.CYAN + 'x_icons': >36}")
        print(f"Çıkış yapmak için {Fore.RED + 'Quit': >37}")
        print(f"Komutları tekrar görmek için {Fore.CYAN + 'Help': >26}")
        print()

    # SauceDemo sitesine git
    # inputları bul
    def open_url(self):
        if self.already_opened:
            return
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.already_opened = True
        # Username alanı bulunana kadar bekle
        # En fazla 10 saniye bekler
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located((By.ID, "user-name")))
        self.username_input = self.driver.find_element(By.ID, "user-name")
        self.password_input = self.driver.find_element(By.ID, "password")
        self.login_btn = self.driver.find_element(By.ID, "login-button")

    # inputları ve actions temizle
    def clear(self, username: bool = True, password: bool = True):
        if username:
            self.username_input.send_keys(Keys.CONTROL + "a")
            self.username_input.send_keys(Keys.DELETE)
        if password:
            self.password_input.send_keys(Keys.CONTROL + "a")
            self.password_input.send_keys(Keys.DELETE)
        self.error_message = ""
        self.actions.reset_actions()

    # Kullanıcı Adı ve Şifre Boş Testi
    def test_invalid_login(self):
        print()
        print(Fore.BLUE + "Kullanıcı Adı ve Şifre Olmadan Giriş Deneniyor")

        # Siteyi aç ve tamamen yüklenmesi için 3 saniye bekle
        self.open_url()

        self.clear()

        self.login_btn.click()

        self.error_message = self.driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3').text

        # Hata mesajının beklediğimiz gibi olup olmadığını kontrol et
        try:
            assert self.error_message == "Epic sadface: Username is required"
            print(Fore.LIGHTGREEN_EX +
                  "=> Kullanıcı Adı ve Şifre Olmadan Giriş Testi BAŞARILI")
        except AssertionError:
            print(Fore.LIGHTRED_EX +
                  "=> Kullanıcı Adı ve Şifre Olmadan Giriş Testi BAŞARISIZ")

    # Şifre boş testi
    def test_invalid_password(self):
        print()
        print(Fore.BLUE + "Şifre Olmadan Giriş Deneniyor")

        self.open_url()
        self.clear()

        self.username_input.send_keys(self.standard_user)

        self.login_btn.click()

        self.error_message = self.driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3').text

        # Hata mesajının beklediğimiz gibi olup olmadığını kontrol et
        try:
            assert self.error_message == "Epic sadface: Password is required"
            print(Fore.LIGHTGREEN_EX +
                  "=> Şifre Olmadan Giriş Testi BAŞARILI")
        except AssertionError:
            print(Fore.LIGHTRED_EX +
                  "=> Şifre Olmadan Giriş Testi BAŞARISIZ")

    # locked_out_user ile giriş yapmayı deneme testi
    def test_locked_out_user(self):
        print()
        print(Fore.BLUE + "locked_out_user ile giriş yapımı deneniyor")

        self.open_url()
        self.clear()

        self.actions.send_keys_to_element(
            self.username_input, self.locked_out_user)
        self.actions.send_keys_to_element(self.password_input, self.password)
        self.actions.perform()

        self.login_btn.click()

        self.error_message = self.driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3').text

        # Hata mesajının beklediğimiz gibi olup olmadığını kontrol et
        try:
            assert self.error_message == "Epic sadface: Sorry, this user has been locked out."
            print(Fore.LIGHTGREEN_EX +
                  "=> locked_out_user ile Giriş Testi BAŞARILI")
        except AssertionError:
            print(Fore.LIGHTRED_EX +
                  "=> locked_out_user ile Giriş Testi BAŞARISIZ")

    # x ikonlarının kaldırıldığını kontrol eden test
    def test_x_icons(self):
        print()
        print(Fore.BLUE + "X ikonları test ediliyor")

        self.open_url()

        self.clear()
        # X ikonlarının belirmesi için Hatalı bir giriş denemesi yapıyorum
        self.login_btn.click()

        # Hata mesajını kapatma butonunu bulup Tıklıyoruz
        # bu butona tıklanınca X ikonlarının kaybolması gerekiyor
        self.driver.find_element(By.CLASS_NAME, "error-button").click()

        # X ikonu varmı diye kontrol ediyoruz
        # Olmaması gerekiyor
        try:
            assert 0 == len(self.driver.find_elements(
                By.CLASS_NAME, "error_icon"))
            print(Fore.LIGHTGREEN_EX +
                  "=> X ikonları Testi BAŞARILI")
        except AssertionError:
            print(Fore.LIGHTRED_EX +
                  "=> X ikonları Testi BAŞARISIZ")

    # Geçerli Kullanıcı ile Giriş yapıp 6 adet ürün olduğunu doğrula
    def test_valid_login(self):
        print()
        print(Fore.BLUE + "Geçerli Kullanıcı Girişi Test ediliyor")

        self.open_url()

        self.clear()

        self.actions.send_keys_to_element(
            self.username_input, self.standard_user)
        self.actions.send_keys_to_element(self.password_input, self.password)
        self.actions.perform()

        self.login_btn.click()

        try:
            assert 6 == len(self.driver.find_elements(
                By.CLASS_NAME, "inventory_item"))
            print(Fore.LIGHTGREEN_EX +
                  "=> Geçerli Kullanıcı Testi BAŞARILI")
        except AssertionError:
            print(Fore.LIGHTRED_EX +
                  "=> Geçerli Kullanıcı Testi BAŞARISIZ")

    def test_all(self):
        self.test_invalid_login()
        self.test_invalid_password()
        self.test_locked_out_user()
        self.test_x_icons()
        self.test_valid_login()
