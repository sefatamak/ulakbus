# -*-  coding: utf-8 -*-
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
""" Personel Modülü

Bu modül Ulakbüs uygulaması için personel modelini ve  personel ile ilişkili modelleri içerir.

"""
from ulakbus.models import Personel, Ceza, HizmetKayitlari
from zengine.forms import JsonForm
from zengine.forms import fields
from zengine.views.crud import CrudView
from zengine.lib.translation import gettext as _, gettext_lazy as __
from zengine import forms
from pyoko import ListNode


class TerfiKontrolForm(forms.JsonForm):
    class Meta:
        inline_edit = ['secim']

    class TerfiListe(ListNode):
        class Meta:
            title = __(u"Personeller")

        secim = fields.Boolean(__(u"Secim"), type="checkbox")
        ad = fields.String(__(u"Ad"))
        soyad = fields.String(__(u"Soyad"))
        key = fields.String(hidden=True)

    terfi_et = fields.Button(__(u"Terfi Et"), cmd="terfi_et")


class TerfiOnayForm(JsonForm):
    onayla = fields.Button(__(u"Onayla"), cmd="onayla")
    iptal = fields.Button(__(u"İptal"), cmd="iptal")


class TerfiKontrol(CrudView):
    class Meta:
        model = "Personel"

    def terfi_kontrol(self):
        personel_list = [hizmet.personel for hizmet in HizmetKayitlari.objects.filter(sebep_kod=None)]
        personel_list = self.ceza_kontrol(personel_list)
        personel_list = self.sicil_kontrol(personel_list)
        personel_list = self.gorev_suresi_kontrol(personel_list)
        self.current.task_data['personel_list'] = [personel.key for personel in personel_list]
        self.current.task_data['terfisi_mevcut'] = bool(personel_list)

    def gorev_suresi_kontrol(self, personeller):
        return filter(lambda personel: self.fiili_hizmet_getir(personel), personeller)

    def fiili_hizmet_getir(personel, self):
        # TODO:Hizmet süresi sabit olarak döndürüldü. Her personele göre fiili_hizmet_getir fonksiyonundan süre döndürülecek.
        return 8

    def ceza_kontrol(self, personeller):
        return filter(lambda personel: not Ceza.objects.filter(personel=personel).count(), personeller)

    def sicil_notu_kontrol(self, personel):
        return True if personel.SicilNot and personel.SicilNot[0].sicil_not > 80 else False

    def sicil_yili_kontrol(self, personel):
        return True if personel.SicilNot[0].sicil_yili.year == 2010 or personel.SicilNot[
                                                                           0].sicil_yili.year == 2009 else False

    def sicil_kontrol(self, personeller):
        return filter(lambda personel: self.sicil_yili_kontrol(personel) and self.sicil_notu_kontrol(personel),
                      personeller)

    def terfi_listesi_goruntule(self):
        self.current.output["meta"]["allow_actions"] = False
        _form = TerfiKontrolForm(title=_(u'Terfisi Gelen Personeller Listesi'))
        for personel_key in self.current.task_data['personel_list']:
            personel = Personel.objects.get(personel_key)
            _form.TerfiListe(ad=personel.ad, soyad=personel.soyad, key=personel_key)
        self.form_out(_form)

    def terfi_onay_form(self):
        self.current.task_data['terfi_list'] = [chosen for chosen in self.input['form']['TerfiListe'] if
                                                chosen['secim']]
        _form = TerfiOnayForm(title="Terfi Onay Form")
        _form.help_text = _("Seçili personellere ait terfi işlemini onaylıyor musunuz?")
        self.form_out(_form)

    def terfi_et(self):
        # TODO:Kademeye göre derece kontrolü yapılacak.
        for personel in self.current.task_data['terfi_list']:
            personel = Personel.objects.get(personel["key"])
            personel.kazanilmis_hak_kademe = personel.kazanilmis_hak_kademe + 1
            personel.blocking_save()

    def terfi_bilgilendirme(self):
        form = JsonForm(title="Terfi Bilgilendirme")
        form.help_text = "Personellere Ait Yeni Terfi Bulunamadı."
        form.tamam = fields.Button(_(u'Ana Menuye Don'))
        self.form_out(form)

    def yonlendir(self):
        self.current.output['cmd'] = 'reload'
