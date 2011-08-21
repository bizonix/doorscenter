# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'SapeAccount.spamTask'
        db.add_column('sapeadmin_sapeaccount', 'spamTask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.SpamTask'], null=True), keep_default=False)

        # Deleting field 'SpamTask.sapeAccount'
        db.delete_column('sapeadmin_spamtask', 'sapeAccount_id')


    def backwards(self, orm):
        
        # Deleting field 'SapeAccount.spamTask'
        db.delete_column('sapeadmin_sapeaccount', 'spamTask_id')

        # User chose to not deal with backwards NULL issues for 'SpamTask.sapeAccount'
        raise RuntimeError("Cannot reverse this migration. 'SpamTask.sapeAccount' and its values cannot be restored.")


    models = {
        'sapeadmin.article': {
            'Meta': {'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Donor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Niche']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'textFile': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'})
        },
        'sapeadmin.donor': {
            'Meta': {'object_name': 'Donor'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Niche']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'})
        },
        'sapeadmin.hosting': {
            'Meta': {'object_name': 'Hosting'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'billingUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'controlUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mainUrl': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'ns1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'ns2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'sapeadmin.hostingaccount': {
            'Meta': {'object_name': 'HostingAccount'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'costPerMonth': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'hosting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Hosting']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'ns1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'ns2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'paymentDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'sapeadmin.niche': {
            'Meta': {'object_name': 'Niche'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'sapeadmin.sapeaccount': {
            'Meta': {'object_name': 'SapeAccount'},
            'WMR': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.WMR']", 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'maxSitesCount': ('django.db.models.fields.IntegerField', [], {'default': '72'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'spamTask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.SpamTask']", 'null': 'True'})
        },
        'sapeadmin.site': {
            'Meta': {'object_name': 'Site'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sapeadmin.Article']", 'null': 'True', 'blank': 'True'}),
            'botsVisitsCount': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'botsVisitsDate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'hostingAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.HostingAccount']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipAddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'linksIndexCount': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'linksIndexDate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Niche']"}),
            'pagesCount': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'sapeAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.SapeAccount']"}),
            'siteIndexCount': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'siteIndexDate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'spamTask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.SpamTask']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'sapeadmin.spamtask': {
            'Meta': {'object_name': 'SpamTask'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'spamDate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'spamLinks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        },
        'sapeadmin.wmid': {
            'Meta': {'object_name': 'WMID'},
            'WMID': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'sapeadmin.wmr': {
            'Meta': {'object_name': 'WMR'},
            'WMID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.WMID']"}),
            'WMR': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'sapeadmin.yandexupdate': {
            'Meta': {'object_name': 'YandexUpdate'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateIndex': ('django.db.models.fields.DateField', [], {}),
            'dateUpdate': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        }
    }

    complete_apps = ['sapeadmin']
