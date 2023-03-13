from colorama import Fore, init
from tabulate import tabulate


def main():
    init(autoreset=True)

    # Öğrencileri tutacağımız liste
    ogrenciler = []

    # Kullanıcıya ilk girişte Hoşgeldiniz mesajı göster
    print(Fore.LIGHTWHITE_EX + "Öğrenci kayıt sistemine hoş geldiniz.")

    # Kullanıcıya kullanabilecek olduğu komutları gösterir
    yardim()

    # Program kullanıcı çıkış yapmak isteyene kadar devam edecek
    while True:
        # Kullanıcıdan gerçekleştirmek istediği komutu alıyoruz
        # Varsa en başta ve en sonda olan boşlukları siliyoruz
        # Komutu küçük harfli haline getiriyoruz
        # Bu sayede kullanıcı ister 'komut', 'KOMUT', veya 'KoMut' girebilir
        print()
        komut = input(
            f"{Fore.LIGHTGREEN_EX + 'Komut giriniz:'} ").strip().lower()
        print()

        # Burada kullanıcının girdiği komut ile bizim desteklediğimiz komutları karşılaştırıyoruz
        # eğer bi karşılaşma bulunursa o komut çalıştırılır
        if komut == "kayıt":
            ogrenci_kayit(ogrenciler)
        elif komut == "sil":
            ogrenci_sil(ogrenciler)
        elif komut == "liste":
            ogrenci_listele(ogrenciler)
        elif komut == "numara":
            ogrenci_numara(ogrenciler)
        elif komut == "çıkış":
            print(Fore.MAGENTA + "Öğrenci Kayıt Sisteminden Çıkılıyor. Güle Güle :)")
            break
        elif komut == "yardım":
            yardim()
        # Kullanıcının girdiği komut bizim komutlarımız arasında yok ise kullanıcı bilgilendirilir
        else:
            print(Fore.RED + "Bilinmeyen bir komut girdiniz!")


def ogrenci_kayit(ogrenci_listesi: list[str]):
    """Kaydı yapılmasını istenilen öğrenci veya öğrencileri, öğrenci listesine ekler

    Arguments:
        ogrenci_listesi -- Kayıtlı öğrencilerin bulunduğu liste
    """

    print(
        Fore.BLUE + "Birden fazla öğrenci kaydı için öğrenci isimleri arasına virgül koyunuz.")
    print(Fore.LIGHTYELLOW_EX + "Örnek: Emir,Recep,Ahmet")
    print()

    # Kullanıcıdan eklemek istediği öğrencinin ismini alıyoruz
    # tek seferde birden fazla öğrenci kaydı yapılmak istenirse
    # virgül(,) kullanarak öğrenci isimlerini ayırmasını istiyoruz
    yeni_ogrenci = input(
        Fore.YELLOW + "=> Eklemek istediğiniz öğrenci veya öğrencilerin isimlerini giriniz: ")

    # eğer girilen değerde virgül var ise
    # o değeri virgüllerinden ayırıyoruz
    # ve isimleri bir listeye saklıyoruz
    if "," in yeni_ogrenci:
        yeni_ogrenci = yeni_ogrenci.split(",")

        # oluşturduğumuz bu listeyi kullanarak
        # öğrencileri tek tek öğrenciler listesine ekliyoruz
        for ogrenci in yeni_ogrenci:
            ogrenci_listesi.append(ogrenci.strip().title())
            print(Fore.LIGHTYELLOW_EX +
                  f"Öğrenci eklendi [{ogrenci.strip().title()}]")
    # eğer girilen değerde virgül yok ise
    # bu kullanıcının sadece 1 kişi eklemek istediği anlamına gelir
    # o kişiyi direkt ekliyoruz
    else:
        ogrenci_listesi.append(yeni_ogrenci.strip().title())
        print(Fore.LIGHTYELLOW_EX +
              f"Öğrenci eklendi [{yeni_ogrenci.strip().title()}]")


def ogrenci_sil(ogrenci_listesi: list[str]):
    """Kaydı silinmesi istenilen öğrenci veya öğrencileri listeden siler

    Arguments:
        ogrenci_listesi -- Kayıtlı öğrencilerin bulunduğu liste
    """

    print(Fore.BLUE + "Lütfen silmek istediğiniz öğrenci veya öğrencilerin adını virgül ile ayırarak giriniz")

    # Kullanıcıdan silmek istediği öğrencinin ismini alıyoruz
    # tek seferde birden fazla öğrenci silmek istenirse
    # virgül(,) kullanarak öğrenci isimlerini ayırmasını istiyoruz
    silinecek_ogrenciler = input(
        Fore.YELLOW + "=> Silinecek öğrenci veya öğrencileri giriniz: ").strip()

    try:
        # eğer girilen değerde virgül var ise
        # o değeri virgüllerinden ayırıyoruz
        # ve isimleri bir listeye saklıyoruz
        if "," in silinecek_ogrenciler:
            silinecek_ogrenciler = [silinecek_ogrenci.strip(
            ).title() for silinecek_ogrenci in silinecek_ogrenciler.split(",")]
            # bu isimleri, öğrenci listemizdeki isimler ile karşılaştırıyoruz
            # isimler uyuşuyor ise bu kişileri siliyoruz
            for silinecek_ogrenci in silinecek_ogrenciler:
                for ogrenci in ogrenci_listesi:
                    if silinecek_ogrenci == ogrenci:
                        ogrenci_listesi.remove(silinecek_ogrenci)
                        print(
                            Fore.RED + f"Öğrenci silindi [{silinecek_ogrenci}]")
        else:
            ogrenci_listesi.remove(silinecek_ogrenciler.title())
            print(
                Fore.RED + f"Öğrenci silindi [{silinecek_ogrenciler.title()}]")
    # girilen isim öğrenciler arasında yok ise kullanıcıyı bilgilendiriyoruz
    except ValueError:
        print(
            Fore.RED + f"Hata: {silinecek_ogrenciler} isminde bir öğrenci bulunmuyor!")


def ogrenci_numara(ogrenci_listesi: list[str]):
    print(Fore.BLUE + "Öğrenci numarasını öğrenmek için lütfen öğrencinin ismini giriniz")
    try:
        # kullanıcıdan numarasını öğrenmek istediği öğrencinin ismini istiyoruz
        ogrenci_ismi = input(Fore.LIGHTYELLOW_EX + "=> Öğrencinin ismini giriniz: ").strip().title()
        print(Fore.YELLOW +
              f"Öğrencinin numarası [{ogrenci_listesi.index(ogrenci_ismi)}]")
    # eğer o isimde bir öğrenci yok ise kullanıcıyı bilgilendiriyoruz
    except ValueError:
        print(Fore.RED + "Hata: Bu isimde öğrenci bulunamadı!")


def ogrenci_listele(ogrenci_listesi: list[str]):
    if len(ogrenci_listesi) < 1:
        print(Fore.LIGHTGREEN_EX + f"Kayıtlarda Gösterilecek Hiç Öğrenci Yok")
        return
    ogrenciler = []
    for index, ogrenci in enumerate(ogrenci_listesi):
        ogrenciler.append((index, ogrenci))
    print(tabulate(ogrenciler, headers=[
          "Numarası", "Öğrenci İsmi"], tablefmt="rounded_grid"))


def yardim():
    # Kullanıcının kullanabileceği komutların listesi
    print()
    print(Fore.LIGHTWHITE_EX + "Kullanabilecek olduğunuz komutlar.")
    print()
    print(f"Yeni öğrenci kaydı için {Fore.BLUE + 'Kayıt': >34}")
    print(f"Öğrenci kaydı silmek için {Fore.LIGHTRED_EX + 'Sil' : >30}")
    print(f"Kayıtlı öğrencileri görmek için {Fore.GREEN + 'Liste' : >26}")
    print(
        f"Bir öğrencinin öğrenci numarasını öğrenmek için {Fore.LIGHTYELLOW_EX + 'Numara'}")
    print(f"Çıkış yapmak için {Fore.RED + 'Çıkış': >40}")
    print(f"Komutları tekrar görmek için {Fore.CYAN + 'Yardım': >30}")
    print()


if __name__ == "__main__":
    main()
