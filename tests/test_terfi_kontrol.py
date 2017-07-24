# -*-  coding: utf-8 -*-
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from zengine.lib.test_utils import BaseTestCase
from ulakbus.models import User


class TestCase(BaseTestCase):
    def test_terfi_kontrol(self):
        user = User.objects.get(username="ulakbus")
        self.prepare_client('/terfi_kontrol', user=user)
        resp = self.client.post()
        assert resp.json['forms']['schema']['title'] == "Terfisi Gelen Personeller Listesi"
        resp = self.client.post(form={'TerfiListe':[{'ad':'İsmail', 'soyad':'Bilgin', 'key':'ZCdSPFxKTK6d8oM7qCVBlwsk5rS', 'secim':True}]},cmd="terfi_et")
        assert resp.json['forms']['schema']['title'] == "Terfi Onay Form"
        resp = self.client.post(form={'iptal': 1})
        assert resp.json['forms']['schema']['title'] == "Terfisi Gelen Personeller Listesi"
        resp = self.client.post(form={'TerfiListe':[{'ad':'İsmail', 'soyad':'Bilgin', 'key':'ZCdSPFxKTK6d8oM7qCVBlwsk5rS', 'secim':True}]},cmd="terfi_et")
        assert resp.json['forms']['schema']['title'] == "Terfi Onay Form"



