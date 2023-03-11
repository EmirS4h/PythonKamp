import random


def main():
    # 1 ile 10 arasında bir sayı üretiyoruz. Kullanıcıdan bu sayıyı tahmin etmesini isteyeceğiz
    secret_number = random.randint(1, 10)

    # Kullanıcının maksimum tahmin hakkı
    life = 3

    # Başlangıç skoru. Kullanıcının her yanlış tahmininde bu skor azalacak
    score = 100

    # Burada sonsuz döngü ile Kullanıcının tahmin hakkı olduğu sürece kullanıcıdan sayıyı tahmin etmesini istiyoruz
    while True:

        # Kullanıcının girdiği Tahminin sayıyıya dönüştürürken hata çıkarsa onu yakalamak için
        # try-except kullanıyoruz
        try:

            # oyun kullanıcının kalan Tahmin hakkı 0 dan büyük olduğu sürece devam edecek
            if life > 0:

                # Kullanıcıdan tahminini girmesini istiyoruz
                # ve girdiyi sayıya çeviriyoruz
                # input methodu girdiyi string olarak döndürür
                # her ne kadar tahmin sırasında örnek olarak 3 de girseniz bu aslında bir string dir
                guess = int(input("Tahmininizi giriniz: "))

                # eğer kullanıcının tahmini ürettiğimiz gizli sayıdan büyük ise
                # kullanıcıya sayının büyük olduğunu belirtiyoruz
                if guess > secret_number:
                    print("Girdiğiniz sayi gizli sayıdan büyük")

                # eğer kullanıcının tahmini ürettiğimiz gizli sayıdan küçük ise
                # kullanıcıya sayının küçük olduğunu belirtiyoruz
                elif guess < secret_number:
                    print("Girdiğiniz sayı gizli sayıdan küçük")

                # eğer üstteki her iki koşulda tutmadıysa o zaman kullanıcı sayıyı doğru tahmin etmiş demektir
                # kullanıcıya sayıyı doğru tahmin ettiğini söyleyip Skorunu belirtiyoruz
                else:
                    print(f"Doğru bildiniz. Skorunuz: [{score}]")
                    # kullanıcı sayıyı doğru tahmin ettiği için break ile oyunu sonlandırıyoruz
                    break

                # eğer kullanıcı sayıyı doğru tahmin edememişse
                # skorundan 10 sayı düşüyoruz
                score -= 10

                # kalan tahmin hakkından da 1 sayı düşüyoruz
                life -= 1

                # ve kullanıcıya geriye kalan tahmin hakkını gösteriyoruz
                print(f"Kalan Tahmin hakkınız {life}")

            # eğer kullanıcının başka tahmin hakkı kalmadıysa
            # kullanıcıya bunu belirtiyor doğru cevabı gösterip oyunu sonlandırıyoruz
            else:
                print(f"Malesef baska Tahmin hakkınız kalmadı.")
                print(f"Doğru cevap {secret_number} olacaktı.")
                break

        # kullanıcının girdiği tahminin sayıya dönüştürme sırasında
        # bir hata alırsak kullanıcıya bunu belirtiyor ve tekrar tahmin etmesini istiyoruz
        except ValueError:
            print("Lütfen bir sayı giriniz!")
            pass


if __name__ == "__main__":
    main()
