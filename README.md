# RaspberryPi_YapayZeka_NesneTanimlama_Seslendirme

Görme engelli kişiler için geliştirdiğim 'nesne tanımlama ve seslendirme robotu' içeriği..

Donanım Kısmında ; RaspberryPi 3B+ , RPi Motor Driver Board , RaspberryPi Kamera Modülü ,
4 Adet DC Motor , 2 Adet Servo Motor ,  4 Adet Tekerlek , Mini Pan/Tilt Kiti (Kamera Tutucu) ,
Mobil Robot Platformu , Hafıza Kartı , Hoparlör , 3 Boyutlu Yazıcı (Robot Kapağı İçin) ,
Powerbank (5 Volt 2 Amper) , Pil (3 Adet 9 Volt) , Bağlantı Kabloları Kullanılmıştır.

Yazılım Kısmında ; Python 3.5 ve Python 2.7 kullanılmıştır. Tensorflow, OpenCV(CV2), Numpy ve
PiCamera kütüphanelerinin kurulumu gerekmektedir.

Geliştirmiş olduğum robot projesine benzer bir ürün veya çalışma henüz piyasada olmadığından ve
bu konuda henüz herhangi bir patent alınmamış olması sebebiyle projenin detaylarını bu aşamada
paylaşamayacağım.

Zamanla; projede kullanmış olduğun yapay zeka eğitimleri ve öğrenimlerini, veri tabanı graflarını,
robot ile hızlı haberleşme algoritmalarını, gps konum takip verileri ve optimizasyonlarını adım adım
paylaşıyor olacağım.

Projenin temeli şu ana maddelere dayanmaktadır;
- Kullanıcı kişinin telefonu ile eşleşme sağlandıktan sonra;
    -> Robot, GPS konum takibi ile görme engelli kişinin yanında hareket eder
    -> Donanıma entegre Pan/Tilt sistemi ile hareketli kamera ile anlık görüntüler alır
    -> Alınan bu anlık görüntüleri daha önceden eğitilmiş veritabanındaki verilerle eşleştirir
    -> Eşleme sağlandıktan sonra kullanıcının isteğine göre; donanıma entegre hoparlör ile veya bir bluetooth
       kulaklık üzerinden çevredeki nesneleri seslendirir.
    -> Bu işlem saniyede ortalama 7 defa tekrar eder.

Not : Geliştirdiğim bu robot; aynı zamanda telefon üzerinden uzaktan kumandalı araba gibi de kullanılabilmektedir.
Görme engelli kişilerin hayatını kolaylaştımanın dışında güvenlik aracı olarak da kullanılabilmektedir.
Oldukça ergonomik ve ufak boyutlara sahip ve bu boyutları sayesinde en ufak noktalara kadar girebilmektedir.
Web üzerinden sağ-sol-ileri-geri olarak 4 yönde hareket ettirilebilen bu robot; kullanım sırasında aynı zamanda
canlı yayın açarak kullanıcıya anlık görüntü sunmaktadır. Tehlikeli olduğu öngörülen yerlere; bu robot sayesinde
uzak mesafelerden görüntü ve bilgi toplanabilmektedir.

Projede hedeflenenler
- Görme engelli kişilerin hayatını kolaylaştırmak
- Askeri anlamda güvenlik tehdidi oluşturan bölgelerde ön araştırma yaparak can kaybını en aza indirmek
- Minimum boyutlarda bir robot üretmemk
- Minimum maliyetle, maksimum fayda sağlamak
