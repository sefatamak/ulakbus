# -*-  coding: utf-8 -*-
#
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from zengine.forms import JsonForm
from zengine.forms import fields
from zengine.views.crud import CrudView
from zengine.lib.translation import gettext as _, gettext_lazy as __
from ulakbus.models import Ceza
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ulakbus.settings import DATE_DEFAULT_FORMAT


class SilOnayForm(JsonForm):
    onayla = fields.Button(__(u"Onayla"), cmd='onayla')
    iptal = fields.Button(__(u"İptal"))


class IdariCezaKontrol(CrudView):
    class Meta:
        model = "Ceza"

    def ceza_kontrol(self):
        ceza_suresi = datetime.now() - relativedelta(years=5)
        self.current.task_data['ceza_sayisi'] = Ceza.objects.filter(baslama_tarihi__lte=ceza_suresi).count()

    def ceza_goruntule(self):
        self.current.output["meta"]["allow_actions"] = True
        self.output['objects'] = [
            [_(u'Ad'), _(u'Soyad'), _(u'Başlangıç Tarihi'), _(u'Bitiş Tarihi'), _(u'Dosya Sıra No'), _(u'Ceza Türü')]]
        ceza_suresi = datetime.now() - relativedelta(years=5)
        for ceza in Ceza.objects.filter(baslama_tarihi__lte=ceza_suresi):
            ad = ceza.personel.ad
            soyad = ceza.personel.soyad
            dosya_sira_no = ceza.dosya_sira_no
            bas_tarihi = ceza.baslama_tarihi.strftime(DATE_DEFAULT_FORMAT) if ceza.baslama_tarihi else ''
            bitis_tarihi = ceza.bitis_tarihi.strftime(DATE_DEFAULT_FORMAT) if ceza.bitis_tarihi else ''
            ceza_turu = ceza.get_takdir_edilen_ceza_display()
            list_item = {
                "fields": [ad, soyad, bas_tarihi, bitis_tarihi, dosya_sira_no, ceza_turu],
                "actions": [
                    {'name': _(u'Sil'), 'cmd': 'sil', 'show_as': 'button',
                     'object_key': 'data_key'}
                ],
                'key': ceza.key}
            self.output['object_title'] = "Ceza Görüntüleme Formu"
            self.output['objects'].append(list_item)

    def ceza_sil_onay_form(self):
        from ulakbus.settings import DATE_DEFAULT_FORMAT
        ceza = Ceza.objects.get(key=self.input['data_key'])
        ad = ceza.personel.ad
        soyad = ceza.personel.soyad
        dosya_sira_no = ceza.dosya_sira_no
        bas_tarihi = ceza.baslama_tarihi.strftime(DATE_DEFAULT_FORMAT) if ceza.baslama_tarihi else ''
        bitis_tarihi = ceza.bitis_tarihi.strftime(DATE_DEFAULT_FORMAT) if ceza.bitis_tarihi else ''
        ceza_turu = ceza.get_takdir_edilen_ceza_display()
        self.current.task_data['object_id'] = self.input['data_key']
        _form = SilOnayForm(title="Ceza Silme Onay Form")
        _form.help_text = _(
            u"""Personel adı: **%(ad)s**
            
            Personel soyadı: **%(soyad)s**
            
            Dosya Sıra No: **%(dosya_sira_no)s**
            
            Ceza Başlangıç Tarihi: **%(bas_tarihi)s**
            
            Ceza Bitiş Tarihi: **%(bitis_tarihi)s**
            
            Ceza Türü: **%(ceza_turu)s**
            
            Bilgilerine sahip cezayı silmek istiyor musunuz ?""") % {
                              'ad': ad, 'soyad': soyad, 'dosya_sira_no': dosya_sira_no, 'bas_tarihi': bas_tarihi,
                              'bitis_tarihi': bitis_tarihi, 'ceza_turu': ceza_turu
                          }
        self.form_out(_form)

    def ceza_sil(self):
        ceza = Ceza.objects.get(key=self.current.task_data['object_id'])
        ceza.blocking_delete()
        del self.current.task_data['object_id']

    def ceza_bilgilendirme(self):
        form = JsonForm(title="Ceza Bilgilendirme Formu")
        form.help_text = "Listelenecek ceza bulunamadı."
        self.form_out(form)
