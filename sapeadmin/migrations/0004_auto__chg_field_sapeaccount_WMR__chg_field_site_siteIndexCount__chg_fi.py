# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'SapeAccount.WMR'
        db.alter_column('sapeadmin_sapeaccount', 'WMR_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.WMR'], null=True))

        # Changing field 'Site.siteIndexCount'
        db.alter_column('sapeadmin_site', 'siteIndexCount', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Site.botsVisitsDate'
        db.alter_column('sapeadmin_site', 'botsVisitsDate', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Site.linksIndexDate'
        db.alter_column('sapeadmin_site', 'linksIndexDate', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Site.siteIndexDate'
        db.alter_column('sapeadmin_site', 'siteIndexDate', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Site.sapeAccount'
        db.alter_column('sapeadmin_site', 'sapeAccount_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.SapeAccount'], null=True))

        # Changing field 'Site.spamTask'
        db.alter_column('sapeadmin_site', 'spamTask_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.SpamTask'], null=True))

        # Changing field 'Site.hostingAccount'
        db.alter_column('sapeadmin_site', 'hostingAccount_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.HostingAccount'], null=True))

        # Changing field 'Site.botsVisitsCount'
        db.alter_column('sapeadmin_site', 'botsVisitsCount', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Site.ipAddress'
        db.alter_column('sapeadmin_site', 'ipAddress', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True))

        # Changing field 'Site.linksIndexCount'
        db.alter_column('sapeadmin_site', 'linksIndexCount', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'SpamTask.spamLinks'
        db.alter_column('sapeadmin_spamtask', 'spamLinks', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'SpamTask.spamDate'
        db.alter_column('sapeadmin_spamtask', 'spamDate', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'HostingAccount.paymentDay'
        db.alter_column('sapeadmin_hostingaccount', 'paymentDay', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'HostingAccount.costPerMonth'
        db.alter_column('sapeadmin_hostingaccount', 'costPerMonth', self.gf('django.db.models.fields.FloatField')(null=True))


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'SapeAccount.WMR'
        raise RuntimeError("Cannot reverse this migration. 'SapeAccount.WMR' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.siteIndexCount'
        raise RuntimeError("Cannot reverse this migration. 'Site.siteIndexCount' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.botsVisitsDate'
        raise RuntimeError("Cannot reverse this migration. 'Site.botsVisitsDate' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.linksIndexDate'
        raise RuntimeError("Cannot reverse this migration. 'Site.linksIndexDate' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.siteIndexDate'
        raise RuntimeError("Cannot reverse this migration. 'Site.siteIndexDate' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.sapeAccount'
        raise RuntimeError("Cannot reverse this migration. 'Site.sapeAccount' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.spamTask'
        raise RuntimeError("Cannot reverse this migration. 'Site.spamTask' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.hostingAccount'
        raise RuntimeError("Cannot reverse this migration. 'Site.hostingAccount' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.botsVisitsCount'
        raise RuntimeError("Cannot reverse this migration. 'Site.botsVisitsCount' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.ipAddress'
        raise RuntimeError("Cannot reverse this migration. 'Site.ipAddress' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Site.linksIndexCount'
        raise RuntimeError("Cannot reverse this migration. 'Site.linksIndexCount' and its values cannot be restored.")

        # Changing field 'SpamTask.spamLinks'
        db.alter_column('sapeadmin_spamtask', 'spamLinks', self.gf('django.db.models.fields.TextField')(default=''))

        # User chose to not deal with backwards NULL issues for 'SpamTask.spamDate'
        raise RuntimeError("Cannot reverse this migration. 'SpamTask.spamDate' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'HostingAccount.paymentDay'
        raise RuntimeError("Cannot reverse this migration. 'HostingAccount.paymentDay' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'HostingAccount.costPerMonth'
        raise RuntimeError("Cannot reverse this migration. 'HostingAccount.costPerMonth' and its values cannot be restored.")


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
            'costPerMonth': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'hosting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Hosting']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'ns1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'ns2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'paymentDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'WMR': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.WMR']", 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'maxSitesCount': ('django.db.models.fields.IntegerField', [], {'default': '81'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'spamTask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.SpamTask']", 'null': 'True'})
        },
        'sapeadmin.site': {
            'Meta': {'object_name': 'Site'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sapeadmin.Article']", 'null': 'True', 'blank': 'True'}),
            'botsVisitsCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'botsVisitsDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'hostingAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.HostingAccount']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipAddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'linksIndexCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'linksIndexDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.Niche']"}),
            'pagesCount': ('django.db.models.fields.IntegerField', [], {'default': '242', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'sapeAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.SapeAccount']", 'null': 'True', 'blank': 'True'}),
            'siteIndexCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'siteIndexDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'spamTask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.SpamTask']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
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
