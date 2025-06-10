# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 19:51:00 2025

@author: Dell
"""
import random
import sys

class Karakter:
    def __init__(self, ad="Çiçekçi"):
        self.ad = ad

class Cicekci(Karakter):
    def __init__(self, ad="Çiçekçi"):
        super().__init__(ad)
        self.can = 24
        self.bakiye = 10
        self.seviye = 1
        self.acik_tohumlar = ["Papatya"]
        self.tohum_stogu = {"Papatya": 2, "Lale": 2}  # Lale tohum stoğu 2
        self.envanter = {}
        self.ekili_alan = {}

    def enerji_harca(self, miktar):
        self.can -= miktar
        if self.can < 0:
            self.can = 0
            print("Canınız bitti!")

    def enerji_kazan(self, miktar):
        self.can += miktar
        if self.can > 100:
            self.can = 100

    def durum_goster(self):
        print(f"{self.ad} - Can: {self.can}, Bakiye: {self.bakiye} TL")
        print("Tohum Stoğu:", self.tohum_stogu)
        print("Çiçek Stoğu:", self.envanter)
        print("Ekili Alan:", self.ekili_alan)

    def markete_git(self):
        if self.can >= 4:
            print("Markete gidiliyor...")
            self.enerji_harca(4)
            return True
        else:
            print("Yeterli canınız yok.")
            return False

    def tohum_al(self, market):
        market.tohumlari_goster(self.acik_tohumlar)
        alinacak_tohum = input("Hangi tohumu almak istersiniz? (Çıkmak için 'q'): ")
        if alinacak_tohum != 'q':
            if alinacak_tohum in market.tohumlar and alinacak_tohum in self.acik_tohumlar:
                fiyat = market.tohumlar[alinacak_tohum][0]
                if self.bakiye >= fiyat:
                    try:
                        adet = int(input(f"Kaç adet {alinacak_tohum} tohumu almak istersiniz?: "))
                    except ValueError:
                        print("Geçersiz sayı.")
                        return False
                    if adet > 0:
                        self.bakiye -= fiyat * adet
                        self.tohum_stogu[alinacak_tohum] = self.tohum_stogu.get(alinacak_tohum, 0) + adet
                        print(f"{adet} adet {alinacak_tohum} tohumu alındı. Yeni bakiye: {self.bakiye} TL")
                        return True
                    else:
                        print("Geçersiz adet.")
                        return False
                else:
                    print("Yeterli bakiyeniz yok.")
                    return False
            else:
                print("Bu tohum markette yok veya henüz seviyeniz yetersiz.")
                return False
        return False

    def cicek_sat(self, market, satilacak_cicek, adet):
        if satilacak_cicek in self.envanter and self.envanter[satilacak_cicek] >= adet:
            satis_fiyati = market.cicek_fiyatlari.get(satilacak_cicek, 0) * adet
            if satis_fiyati > 0:
                self.bakiye += satis_fiyati
                self.envanter[satilacak_cicek] -= adet
                self.enerji_kazan(adet * 10)
                print(f"{adet} adet {satilacak_cicek} satıldı. Kazanılan para: {satis_fiyati} TL. Yeni bakiye: {self.bakiye} TL. Can arttı.")
                return True
            else:
                print("Bu çiçeğin satış fiyatı bulunamadı.")
                return False
        else:
            print(f"Envanterinizde yeterli miktarda {satilacak_cicek} yok.")
            return False

    def seviye_atla(self, market):
        self.seviye += 1
        self.can = 24  # Her seviyede can sayısını 24 yapıyoruz.
        if self.seviye < 11:
            yeni_acilan_tohum = market.tohum_listesi[self.seviye - 1]
            self.acik_tohumlar.append(yeni_acilan_tohum)
            print(f"Tebrikler! {self.seviye}. levele geçtiniz. Artık {yeni_acilan_tohum} tohumunu markette alabilirsiniz.")
            return False
        else:
            print("Tebrikler! Oyunu bitirip kazandınız!")
            return True

    def tohum_ek(self):
        """Ekim yapmak için tohum stoğundan en az birinin bulunması yeterli olacak"""
        if any(stok > 0 for stok in self.tohum_stogu.values()):  # Tohum stoklarından herhangi birinin 1'den büyük olması yeterli
            print("Ekim yapılıyor...")
            for tohum, stok in self.tohum_stogu.items():
                if stok > 0:
                    self.tohum_stogu[tohum] -= 1  # Ekim yapılan tohum stoğundan bir adet düşürülür
                    self.ekili_alan[tohum] = self.ekili_alan.get(tohum, 0) + 1
                    self.enerji_harca(6)
                    self.bakiye -= 5  # Ekim maliyeti
                    print(f"{tohum} ekildi.")
                    return True
            print("Ekim yapılacak tohum bulunamadı.")
            return False
        else:
            print("Tohum stoğunuzda hiç tohum yok!")
            return False


class Market:
    def __init__(self):
        self.tohum_listesi = ["Papatya", "Lale", "Gül", "Orkide", "Menekşe", "Karanfil", "Zambak", "Ayçiçeği", "Begonya", "Gelincik"]
        self.tohumlar = {
            "Papatya": (10, "🌼"),
            "Lale": (20, "🌷"),
            "Gül": (30, "🌹"),
            "Orkide": (40, "🌸"),
            "Menekşe": (50, "💜"),
            "Karanfil": (60, "💐"),
            "Zambak": (70, "🤍"),
            "Ayçiçeği": (80, "🌻"),
            "Begonya": (90, "🌺"),
            "Gelincik": (100, "🏵️")
        }
        self.cicek_fiyatlari = {
            "Papatya": 15,
            "Lale": 25,
            "Gül": 35,
            "Orkide": 45,
            "Menekşe": 55,
            "Karanfil": 65,
            "Zambak": 75,
            "Ayçiçeği": 85,
            "Begonya": 95,
            "Gelincik": 105
        }

    def tohumlari_goster(self, acik_tohumlar):
        print("\n--- Tohumlar ---")
        for ad, fiyat_emoji in self.tohumlar.items():
            if ad in acik_tohumlar:
                print(f"{ad}: {fiyat_emoji[0]} TL {fiyat_emoji[1]}")
        print("-----------------")
