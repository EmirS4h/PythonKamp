# Pytest Decorators
    
- ### @pytest.fixture: 
   Bu dekorator fixture tanımlamak için kullanılır, fixture'ler test fonksiyonlarına veri sağlayan fonksiyonlardır. Fixture'ler testler için ön koşul oluşturma, veri sağlama veya temizleme için kullanılabilir.

- ### @pytest.mark.parametrize: 
  Bu fixture bir test fonksiyonunu farklı parametreler ile birden fazla test etmek için kullanılır.

- ### @pytest.mark.skip: 
  Bu fixture bir test fonksiyonun es geçmek için kullanılır.

- ### @pytest.mark.xfail: 
  Bu fixture test fonksiyonun başarısız olması beklendiği zaman kullanılır.

- ### @pytest.mark.timeout: 
  Bu fixture bir teste çalışması için belli bir süre tanımlamamızı sağlar.
  Yavaş yada verimsiz testleri belirlememize yardımcı olur.

- ### @pytest.mark.order: 
  Testlerin hangi sırayla çalışması gerektiğini ayarlamamızı sağlar.

- ### @pytest.mark.usefixtures: 
  Bu fixture ile test fonksiyonumuzun hangi fixture'leri kullanması gerektiğini belirleriz.
  