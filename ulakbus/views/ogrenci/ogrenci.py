# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

import random
from pyoko import form
from zengine.lib.forms import JsonForm
from zengine.views.crud import CrudView
from ulakbus.services.zato_wrapper import MernisKimlikBilgileriGetir
from ulakbus.services.zato_wrapper import KPSAdresBilgileriGetir


class KimlikBilgileriForm(JsonForm):
    class Meta:
        include = ['tckn', "ogrenci_no", "ad", "soyad", "cinsiyet", "dogum_tarihi", "dogum_yeri", "uyruk",
                   "medeni_hali", "baba_adi", "ana_adi", "cuzdan_seri", "cuzdan_seri_no", "kayitli_oldugu_il",
                   "kayitli_oldugu_ilce", "kayitli_oldugu_mahalle_koy", "kayitli_oldugu_cilt_no",
                   "kayitli_oldugu_aile_sıra_no", "kayitli_oldugu_sira_no", "kimlik_cuzdani_verildigi_yer",
                   "kimlik_cuzdani_verilis_nedeni", "kimlik_cuzdani_kayit_no", "kimlik_cuzdani_verilis_tarihi"]

    kaydet = form.Button("Kaydet", cmd = "save")
    mernis_sorgula = form.Button("Mernis Sorgula", cmd="mernis_sorgula")

<<<<<<< HEAD

class IletisimBilgileriForm(JsonForm):
    class Meta:
        include = ["ikamet_adresi", "e_posta", "tel_no"]

    kaydet = form.Button("Kaydet", "save")


=======
>>>>>>> Öğrenci iletişim bilgileri kayıt işlemi gerçekleştirildi
class KimlikBilgileri(CrudView):
    class Meta:
        model = "Ogrenci"

    def kimlik_bilgileri(self):
        self.form_out(KimlikBilgileriForm(self.object, current=self.current))

    def mernis_sorgula(self):
        servis = MernisKimlikBilgileriGetir(tckn=self.object.tckn)
        kimlik_bilgisi = servis.zato_request()
        self.object(**kimlik_bilgisi)
        self.object.save()
<<<<<<< HEAD
=======

class IletisimBilgileriForm(JsonForm):
    class Meta:
        include = ["ikamet_il", "ikamet_ilce", "ikamet_adresi", "posta_kodu", "eposta", "tel_no"]

    kaydet = form.Button("Kaydet", cmd="save")
    kps_sorgula = form.Button("KPS Sorgula", cmd="kps_sorgula")

class IletisimBilgileri(CrudView):
    class Meta:
        model = "Ogrenci"

    def iletisim_bilgileri(self):
        self.form_out(IletisimBilgileriForm(self.object, current = self.current))

    def kps_sorgula(self):
        servis = KPSAdresBilgileriGetir(tckn = self.object.tckn)
        iletisim_bilgisi = servis.zato_request()
        self.object(**iletisim_bilgisi)
        self.object.save()
>>>>>>> Öğrenci iletişim bilgileri kayıt işlemi gerçekleştirildi
