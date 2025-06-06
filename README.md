# Gercek-Zamanli-Sozdizimi-Vurgulayici-
# Özet
Bu çalışma, gerçek zamanlı bir sözdizimi vurgulayıcısı geliştirmeyi amaçlamaktadır. Python dili kullanılarak geliştirilen bu sistem, kullanıcının yazdığı kodu anlık olarak analiz ederek dilbilgisel olarak doğru yapıları renklendirirken hatalı yapıları altını çizerek belirtmektedir. 
# Yöntem
Projede öncelikle lexer (sözcüksel analizci) geliştirilmiştir. Bu lexer, oluşturulan dile ait anahtar kelimeleri (if, while, print, var vb.), operatörleri (+, -, =, <, >), parantezleri ve diğer yapıları tanıyacak şekilde tanımlanmıştır.
Daha sonra, parser modülü ile dilin gramerine uygun cümle yapıları doğrulanmıştır. Örneğin bir atama ifadesi, önce "var" kelimesi, sonra bir değişken ismi, ardından "=" ve bir ifade ile tanımlanmalıdır. İfade yapıları için özyineli (recursive descent) analiz uygulanmıştır.
images/Ekran görüntüsü 2025-06-06 175929.png
# Gerçekleştirim
Kodlama Python 3 ile yapılmıştır. Kullanıcı arayüzü için Tkinter kütüphanesi tercih edilmiştir. Ana pencerede bir metin kutusu bulunmakta ve kullanıcının her yazdığı karakter sonrasında lexer ve parser çalışmaktadır.
Doğru yazılan anahtar kelimeler yeşil, ifadeler mavi renkte vurgulanmakta; sözdizimsel hatalar ise kırmızı altı çizili şekilde görüntülenmektedir. Örneğin eksik tırnağı olan bir string ya da kapanmamış bir parantez anlık olarak tespit edilip belirtilmektedir.
# Videosu
https://youtu.be/874nrnJCpPs
# Sonuç ve Değerlendirme
Bu proje ile, kodlama süreci sırasında yapılan hataların anlık olarak fark edilebilmesi sağlanmıştır.Sistem, küçük ve basit diller için etkili bir öğretim aracı olarak tasarlanmıştır. 
# Kaynaklar
1.	Aho, Lam, Sethi, Ullman - Compilers: Principles, Techniques, and Tools.
2.	Python Resmi Belgeleri - https://docs.python.org
3.	Tkinter Kullanım Kılavuzu - https://tkdocs.com
