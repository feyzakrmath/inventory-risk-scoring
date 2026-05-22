# RİSK SCORE MODEL

# AMAÇ
 Üretilmiş sentetik veri kullanarak, son kullanma tarihinden önce atığa dönüşme riski taşıyan envanter lotları için açıklanabilir matematiksel risk skor modeli oluşturmak.
# CONTEXT 
envanter veri seti;

snapshot_ts
store_id
sku
product_name
on_hand_qty
expiry_date
lot_id
purchased_date
unit_cost_at_lot

# 1 inevntory datası
Ürünlerin kalan raf ömrünü gösteren tablo elde edildi.
max 3649 gün , min 6 gün olarak çıktı alındı; en kritik ürün ve 10 yıldan fazla raf ömrü olan ürünler gözlemlendi.
# days_to_expiry = expiry_date - snapshot_ts #

# 2 daily velocity
bir ürün bu mağazada günlük ortalama kaç adet satılıyor bunu gösteren tablo elde edildi.
Toplam satış miktarınım mağaza-ürün bazında gruplanması ve 15 günlük satış penceresine bölünmesiyle hesaplanmıştır.
ortalama günlük talebi de tahmin eder.
# daily_velocity = total_qty / 15 #

# 3 coverage hesaplama
stok sayısını günlük satış hızına bölerek hesaplanmıştır.
Kaç stok var, expiry ne zaman demek yerine doğrudan bu ürün expiry olmadan bitecek mi? bunu cevaplaması amaçlanmıştır.
coverage < expiry ise güvenli 
coverage > expiry ise riskli 
coverage = expiry ise orta 
yüksek coverage ile düşük kalan raf ömrünün birleşmesi yüksek atık riski demektir.
Aşırı uç değerleri kontrol altına almak için coverage değerleri maksimum 365 gün ile sınırlandırılmıştır.
# coverage_days = on_hand_qty / daily_velocity #

# 4 Risk Score Formula
Model için temel yapıyı oluşturacak formül core_risk = coverage_days / (days_to_expiry + 1) şeklinde.
Eğer tahmini stok tüketim süresi kalan raf ömründen uzunsa, ürünün satılmadan önce son kullanma tarihine ulaşma ihtimali yüksektir.
Stok değerleri farklı olabilir, yüksek değerler modeli domine edebilir b u yüzden stock normalize edildi.
Final risk formulü = 0.8 * core_risk + 0.2 * stock_norm şeklinde.
riskin ana belirleyicisi coverage ve expiry ilişkisi  yani operasyonel uygulanabilirlik olsun istediğim için 0.8 ini buna verdim, stok miktarı da yine 0.2 etkilesin istedim.

# Risk seviye etiketleri
Bir fonksiyon tanımlayarak hesaplanan risk skoru kategorize edildi.
skor düşükse x < 0.5 low etiketi
skor ortaysa  0.5 <= x < 1 ise medium etiketi
skor yüksekse x > 1 ise high etiketi

# NOT
Yüksek riskli envanter kayıtları genellikle:
düşük satış hızına
yüksek coverage değerine
kısa kalan raf ömrüne sahiptir.

Model, son kullanma tarihinden önce satılma ihtimali düşük olan lotları başarılı şekilde tespit etmektedir.

