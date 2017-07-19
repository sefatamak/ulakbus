# -*-  coding: utf-8 -*-
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from ulakbus.models import User, Ceza
from zengine.lib.test_utils import BaseTestCase
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TestCase(BaseTestCase):
    def test_idari_ceza_kontrol(self):
        user = User.objects.get(username="ulakbus")
        self.prepare_client('/idari_ceza_kontrol', user=user)
        resp = self.client.post()
        ceza_suresi = datetime.now() - relativedelta(years=5)
        ceza_sayisi = Ceza.objects.filter(baslama_tarihi__lte=ceza_suresi).count()
        if ceza_sayisi > 0:
            assert resp.json['object_title'] == "Ceza Görüntüleme Formu"
            resp = self.client.post(cmd="sil", data_key="2rlWHRkLJfxpvzVFjl4SDZmJWGN")
            assert resp.json['forms']['schema']['title'] == "Ceza Silme Onay Form"
            resp = self.client.post(form={'iptal': 1})
            assert resp.json['object_title'] == "Ceza Görüntüleme Formu"
            assert Ceza.objects.filter(baslama_tarihi__lte=ceza_suresi).count() == ceza_sayisi
            resp = self.client.post(cmd="sil", data_key="2rlWHRkLJfxpvzVFjl4SDZmJWGN")
            assert resp.json['forms']['schema']['title'] == "Ceza Silme Onay Form"
            resp = self.client.post(form={'onayla': 1}, cmd="onayla")
            assert Ceza.objects.filter(baslama_tarihi__lte=ceza_suresi).count() == ceza_sayisi - 1
            if Ceza.objects.filter(baslama_tarihi__lte=ceza_suresi).count() > 0:
                assert resp.json['object_title'] == "Ceza Görüntüleme Formu"
        else:
            assert resp.json['forms']['schema']['title'] == "Ceza Bilgilendirme Formu"
