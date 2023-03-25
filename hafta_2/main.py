from saucedemo import SauceDemo


def main():
    test_class = SauceDemo()
    print()
    print("----- Test Sauce Demo'ya Hoşgeldiniz -----")
    test_class.avaliable_commands()
    while True:
        try:
            komut = input("Test komutu giriniz: ").lower()
            match komut:
                case "all":
                    test_class.test_all()
                case "valid_login":
                    test_class.valid_login()
                case "invalid_login":
                    test_class.test_invalid_login()
                case "invalid_password":
                    test_class.test_invalid_password()
                case "locked_out_user":
                    test_class.test_locked_out_user()
                case "x_icons":
                    test_class.test_x_icons()
                case "help":
                    test_class.avaliable_commands()
                case "quit":
                    break
                case _:
                    print("Böyle bir Test bulunamadı.")
                    continue
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
