# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Hosting'
        db.create_table('sapeadmin_hosting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('mainUrl', self.gf('django.db.models.fields.URLField')(default='http://', max_length=200, blank=True)),
            ('controlUrl', self.gf('django.db.models.fields.URLField')(default='http://', max_length=200, blank=True)),
            ('billingUrl', self.gf('django.db.models.fields.URLField')(default='http://', max_length=200, blank=True)),
            ('ns1', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('ns2', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
        ))
        db.send_create_signal('sapeadmin', ['Hosting'])

        # Adding model 'HostingAccount'
        db.create_table('sapeadmin_hostingaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('hosting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.Hosting'])),
            ('login', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('ns1', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('ns2', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('costPerMonth', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('paymentDay', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('sapeadmin', ['HostingAccount'])

        # Adding model 'Niche'
        db.create_table('sapeadmin_niche', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal('sapeadmin', ['Niche'])

        # Adding model 'Donor'
        db.create_table('sapeadmin_donor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.Niche'])),
            ('url', self.gf('django.db.models.fields.URLField')(default='http://', max_length=200)),
        ))
        db.send_create_signal('sapeadmin', ['Donor'])

        # Adding model 'Article'
        db.create_table('sapeadmin_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.Niche'])),
            ('donor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.Donor'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('textFile', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
        ))
        db.send_create_signal('sapeadmin', ['Article'])

        # Adding model 'Site'
        db.create_table('sapeadmin_site', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.Niche'])),
            ('pagesCount', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('ipAddress', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
            ('hostingAccount', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.HostingAccount'])),
            ('sapeAccount', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.SapeAccount'])),
            ('spamTask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.SpamTask'])),
            ('linksIndexCount', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('linksIndexDate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('botsVisitsCount', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('botsVisitsDate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('siteIndexCount', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('siteIndexDate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal('sapeadmin', ['Site'])

        # Adding M2M table for field articles on 'Site'
        db.create_table('sapeadmin_site_articles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('site', models.ForeignKey(orm['sapeadmin.site'], null=False)),
            ('article', models.ForeignKey(orm['sapeadmin.article'], null=False))
        ))
        db.create_unique('sapeadmin_site_articles', ['site_id', 'article_id'])

        # Adding model 'SapeAccount'
        db.create_table('sapeadmin_sapeaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('login', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('email', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('hash', self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True)),
            ('maxSitesCount', self.gf('django.db.models.fields.IntegerField')(default=92)),
            ('WMR', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.WMR'], blank=True)),
        ))
        db.send_create_signal('sapeadmin', ['SapeAccount'])

        # Adding model 'SpamTask'
        db.create_table('sapeadmin_spamtask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('spamDate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('spamLinks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sapeAccount', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.SapeAccount'], blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal('sapeadmin', ['SpamTask'])

        # Adding model 'WMID'
        db.create_table('sapeadmin_wmid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('WMID', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal('sapeadmin', ['WMID'])

        # Adding model 'WMR'
        db.create_table('sapeadmin_wmr', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('WMR', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('WMID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sapeadmin.WMID'])),
        ))
        db.send_create_signal('sapeadmin', ['WMR'])

        # Adding model 'YandexUpdates'
        db.create_table('sapeadmin_yandexupdates', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('dateUpdate', self.gf('django.db.models.fields.DateField')()),
            ('dateIndex', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('sapeadmin', ['YandexUpdates'])


    def backwards(self, orm):
        
        # Deleting model 'Hosting'
        db.delete_table('sapeadmin_hosting')

        # Deleting model 'HostingAccount'
        db.delete_table('sapeadmin_hostingaccount')

        # Deleting model 'Niche'
        db.delete_table('sapeadmin_niche')

        # Deleting model 'Donor'
        db.delete_table('sapeadmin_donor')

        # Deleting model 'Article'
        db.delete_table('sapeadmin_article')

        # Deleting model 'Site'
        db.delete_table('sapeadmin_site')

        # Removing M2M table for field articles on 'Site'
        db.delete_table('sapeadmin_site_articles')

        # Deleting model 'SapeAccount'
        db.delete_table('sapeadmin_sapeaccount')

        # Deleting model 'SpamTask'
        db.delete_table('sapeadmin_spamtask')

        # Deleting model 'WMID'
        db.delete_table('sapeadmin_wmid')

        # Deleting model 'WMR'
        db.delete_table('sapeadmin_wmr')

        # Deleting model 'YandexUpdates'
        db.delete_table('sapeadmin_yandexupdates')


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
            'url': ('django.db.models.fields.URLField', [], {'default': "'http://'", 'max_length': '200'})
        },
        'sapeadmin.hosting': {
            'Meta': {'object_name': 'Hosting'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'billingUrl': ('django.db.models.fields.URLField', [], {'default': "'http://'", 'max_length': '200', 'blank': 'True'}),
            'controlUrl': ('django.db.models.fields.URLField', [], {'default': "'http://'", 'max_length': '200', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mainUrl': ('django.db.models.fields.URLField', [], {'default': "'http://'", 'max_length': '200', 'blank': 'True'}),
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
            'maxSitesCount': ('django.db.models.fields.IntegerField', [], {'default': '92'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
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
            'sapeAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sapeadmin.SapeAccount']", 'blank': 'True'}),
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
        'sapeadmin.yandexupdates': {
            'Meta': {'object_name': 'YandexUpdates'},
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
