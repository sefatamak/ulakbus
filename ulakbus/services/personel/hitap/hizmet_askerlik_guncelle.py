# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

"""HITAP Askerlik Guncelle

Hitap'a personelin askerlik bilgilerinin eklenmesini yapar.

"""

__author__ = 'H.İbrahim Yılmaz (drlinux)'

from ulakbus.services.personel.hitap.hitap_guncelle import HITAPGuncelle


class HizmetAskerlikGuncelle(HITAPGuncelle):
    """
    HITAP Guncelleme servisinden kalıtılmış Hizmet Askerlik Bilgisi Guncelleme servisi

    """

    def handle(self):
        """Servis çağrıldığında tetiklenen metod.

        Attributes:
            service_name (str): İlgili Hitap sorgu servisinin adı
            service_dict (dict): Request yoluyla gelen kayıtlar,
                    HizmetAskerlikUpdate servisinin alanlarıyla eşlenmektedir.
                    Filtreden geçecek tarih alanları ve gerekli alanlar listede tutulmaktadır.
        """

        self.service_name = 'HizmetAskerlikUpdate'
        self.service_dict = {
            'fields': {
                'kayitNo': self.request.payload['kayit_no'],
                'askerlikNevi': self.request.payload['askerlik_nevi'],
                'baslamaTarihi': self.request.payload['baslama_tarihi'],
                'bitisTarihi': self.request.payload['bitis_tarihi'],
                'kitaBaslamaTarihi': self.request.payload['kita_baslama_tarihi'],
                'kitaBitisTarihi': self.request.payload['kita_bitis_tarihi'],
                'muafiyetNeden': self.request.payload['muafiyet_neden'],
                'sayilmayanGunSayisi': self.request.payload['sayilmayan_gun_sayisi'],
                'sinifOkuluSicil': self.request.payload['sinif_okulu_sicil'],
                'subayliktanErligeGecisTarihi': self.request.payload[
                    'subayliktan_erlige_gecis_tarihi'],
                'subayOkuluGirisTarihi': self.request.payload['subay_okulu_giris_tarihi'],
                'tckn': self.request.payload['tckn'],
                'tegmenNaspTarihi': self.request.payload['tegmen_nasp_tarihi'],
                'gorevYeri': self.request.payload['gorev_yeri'],
                'kurumOnayTarihi': self.request.payload['kurum_onay_tarihi'],
                'astegmenNaspTarihi': self.request.payload['astegmen_nasp_tarihi']
            },
            'date_filter': ['baslamaTarihi', 'bitisTarihi', 'kitaBaslamaTarihi', 'kitaBitisTarihi',
                            'subayliktanErligeGecisTarihi', 'subayOkuluGirisTarihi',
                            'tegmenNaspTarihi', 'kurumOnayTarihi', 'astegmenNaspTarihi'],
            'required_fields': ['kayitNo', 'tckn', 'askerlikNevi', 'kurumOnayTarihi']
        }
        super(HizmetAskerlikGuncelle, self).handle()