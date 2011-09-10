# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'SapeAccount', fields ['login']
        db.create_unique('sapeadmin_sapeaccount', ['login'])

        # Adding unique constraint on 'Article', fields ['url']
        db.create_unique('sapeadmin_article', ['url'])

        # Adding unique constraint on 'Site', fields ['url']
        db.create_unique('sapeadmin_site', ['url'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Site', fields ['url']
        db.delete_unique('sapeadmin_site', ['url'])

        # Removing unique constraint on 'Article', fields ['url']
        db.delete_unique('sapeadmin_article', ['url'])

        # Removing unique constraint on 'SapeAccount', fields ['login']
        db.delete_unique('sapeadmin_sapeaccount', ['login'])


    models = {
        'sapeadmin.article': {
            'Meta': {'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Donor']", 'null': 'True'}),
            'fileDigest': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'fileName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'unique': 'True', 'max_length': '200'})
        },
        'sapeadmin.donor': {
            'Meta': {'object_name': 'Donor'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'unique': 'True', 'max_length': '200'})
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
            'costPerMonth': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'hosting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Hosting']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'ns1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'ns2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'paidTill': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'sapeadmin.niche': {
            'Meta': {'object_name': 'Niche'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '10', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'sapeadmin.sapeaccount': {
            'Meta': {'object_name': 'SapeAccount'},
            'WMR': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.WMR']", 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '50'}),
            'maxSitesCount': ('django.db.models.fields.IntegerField', [], {'default': '83'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'sapeadmin.site': {
            'Meta': {'object_name': 'Site'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sapeadmin.Article']", 'null': 'True', 'blank': 'True'}),
            'botsVisitsCount': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'botsVisitsDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bulkAddSites': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'hostingAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.HostingAccount']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipAddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'linksIndexCount': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'linksIndexDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Niche']", 'null': 'True'}),
            'pagesCount': ('django.db.models.fields.IntegerField', [], {'default': '289', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'sapeAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.SapeAccount']", 'null': 'True', 'blank': 'True'}),
            'siteIndexCount': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'siteIndexDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'spamTask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.SpamTask']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'sapeadmin.spamtask': {
            'Meta': {'object_name': 'SpamTask'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'spamDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'spamLinks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'WMID': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.WMID']", 'null': 'True'}),
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
            'dateIndex': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'dateUpdate': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        }
    }

    complete_apps = ['sapeadmin']
