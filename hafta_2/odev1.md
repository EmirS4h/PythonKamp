# HTML
Html açılımı Hyper Text Markup Language'dir. Web sitelerinin temelini oluşturan bir işaretleme dilidir.
Html web tarayıcıları tarafından yorumlanarak kullanıcılara görüntüleyebileceği şekilde sunulur.

# HTML LOCATORS
Web sayfalarında yer alan öğelere erişmek için kullanılan yöntemlerdir.
Selenium gibi otomasyon araçları kullanırken veya web sitesi yaparken siteye şekil ve işlevsellik katmak için kullanılabilir.
5 farklı şekilde olabilir:

- Id: Öğelerin benzersiz bir kimliğe sahip olmasını sağlar, ID ile Html elementine erişilebilir.
- Name: Öğelere kullanabilecek olduğumuz isimler vermemizi sağlar.
- Class: Genelde css ile öğeye şekil vermek için kullanılır, aynı zamanda erişim içinde kullanılabilir.
- Tag: Tagler öğelerin etiketleridir, bu etiketleri kullanarak öğeye erişilebilir.
- XPath: Öğenin Html kodları içerisindeki yolunu belirler, bu yol kullanılarak öğeye erişilebilinir.
  
# Seleniumda Aksiyonlar
Selenium kullanırken ulaştığımız öğe üzerinde bazı aksiyonlar gerçekleştirebiliriz
Bunlar:

- click(): Seçili öğeye tıklar
- clickAndHold(): Seçili öğeye tıklar ve basılı bir şekilde bekler
- doubleClick(): Seçili öğeye çift tıklar
- clear(): Seçili öğenin text kısmını temizler
- sendKeys(): Parantez içerisine girilen değeri, seçili öğenin içerisine girer
