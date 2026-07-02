# Ödeme Kontrollü Sevkiyat (payment_control_shipping)

Ödemesi/faturası tamamlanmamış müşteri siparişlerinin sevkiyatını, esnek bir
onay mekanizmasıyla kontrol altına alan Odoo 15 modülü.

- **Sürüm:** 15.0.3.0.0
- **Odoo:** 15.0
- **Lisans:** LGPL-3
- **Geliştirici:** Alper Tofta

---

## Ne yapar?

Bir müşteri sevkiyatı (çıkış transferi) doğrulanırken, bağlı satış siparişinin
ödeme/fatura durumunu kontrol eder. Ödeme tamamlanmamışsa sevkiyat doğrulanamaz.
İstisnai durumlar için, yetkili kişilerin onayıyla sevkiyata izin verilebilir.

Kontrol yalnızca **satış siparişine bağlı çıkış (outgoing) transferlerinde**
çalışır. Mal kabul, iç transfer, üretim ve satışa bağlı olmayan hareketler
etkilenmez.

---

## Özellikler

- **Ödeme kontrolü:** Faturası kesilmemiş veya ödemesi tamamlanmamış siparişin
  sevkiyatı engellenir (`paid` / `in_payment` durumları geçerli sayılır).
- **Onay mekanizması:** Ödemesiz sevkiyat için, talep eden kişi onaycı seçip
  onay ister. Onay sipariş bazında saklanır; onaylanan siparişin tüm
  sevkiyatları (backorder'lar dâhil) muaf olur.
- **Çok kanallı bildirim:** Onay talebi seçilen onaycılara e-posta + SMS +
  Odoo aktivitesi olarak iletilir; mail ve SMS, doğrudan ilgili siparişe giden
  bağlantı içerir.
- **Zorunlu açıklamalı onay/red:** Onaycı, zorunlu gerekçe girerek onaylar ya da
  reddeder. Her karar "Emin misiniz?" onayıyla korunur.
- **Denetim izi:** Talep, onay, red, sıfırlama ve onaycı geçişleri sipariş/
  sevkiyat sohbet (chatter) alanına otomatik yazılır.
- **Onaycı grubu:** "Sevkiyat Onaycısı" grubundaki kullanıcılar ödeme kontrolünü
  doğrudan geçebilir (iz bırakılarak).
- **Kriz modu:** Yöneticiler, Ayarlar'dan tek tıkla kontrolü geçici olarak
  tümüyle devre dışı bırakabilir.

---

## Bağımlılıklar

`stock`, `sale_stock`, `account`, `mail`, `sms`

---

## Kurulum

1. Modülü Odoo `addons` yoluna ekleyin.
2. Uygulamalar > **Uygulama Listesini Güncelle**.
3. **Ödeme Kontrollü Sevkiyat** modülünü kurun (veya güncellemede *Yükselt*).

---

## Yapılandırma

### 1. Onaycıları tanımlayın
**Ayarlar > Kullanıcılar** üzerinden ilgili kişilere **"Sevkiyat Onaycısı"**
grubunu verin. Her birim için en az bir onaycı önerilir.

### 2. Bildirim ön koşulları
- **E-posta** için geçerli bir giden e-posta (SMTP) sunucusu tanımlı olmalı ve
  onaycıların e-posta adresi dolu olmalı.
- **SMS** için çalışan bir SMS sağlayıcısı yapılandırılmış olmalı ve onaycıların
  cep (mobil) numarası dolu olmalı.

### 3. Kriz modu (aç/kapa)
**Ayarlar > Envanter > Ödeme Kontrolü** bölümündeki **"Ödeme Kontrollü Sevkiyat
Aktif"** kutusu ile kontrol açılıp kapatılabilir. Kapatıldığında tüm
sevkiyatlarda kontrol geçici olarak devre dışı kalır. Yalnızca Ayarlar
yetkisine sahip kullanıcılar görür.

---

## Kullanım Akışı

1. Ödemesi/faturası tamamlanmamış bir sevkiyat doğrulanmak istendiğinde işlem
   engellenir ve açıklayıcı bir uyarı gösterilir.
2. **Ödeme Onayı İste** ile onay istenecek kişiler seçilir; seçilenlere
   bağlantılı e-posta + SMS + aktivite gider.
3. Onaycı, bağlantıdan siparişe gidip **Ödeme Onayı Kararı** ile zorunlu açıklama
   girerek **Onaylar** veya **Reddeder**.
4. Onaylandığında ilgili kullanıcı sevkiyatı tekrar **Doğrula** ile tamamlar.
5. Onaycı grubundaki kullanıcılar, onay adımına gerek kalmadan doğrudan
   doğrulayabilir (bu geçişler iz bırakır).

Ödeme ve fatura zaten tamamsa hiçbir onay adımına girilmez; sevkiyat normal
şekilde doğrulanır.

---

## Notlar

- Kararlar geri alınabilir: onaycı **"Onay Durumunu Sıfırla"** ile durumu
  başa döndürebilir. Tüm işlemler chatter'da izlenebilir.
- Satış siparişine bağlı olmayan manuel çıkışlar bu modülün kapsamı dışındadır.
