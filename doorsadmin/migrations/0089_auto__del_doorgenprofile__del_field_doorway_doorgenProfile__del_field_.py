# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'DoorgenProfile'
        db.delete_table('doorsadmin_doorgenprofile')

        # Deleting field 'Doorway.doorgenProfile'
        db.delete_column('doorsadmin_doorway', 'doorgenProfile_id')

        # Deleting field 'Net.doorgenProfile'
        db.delete_column('doorsadmin_net', 'doorgenProfile_id')


    def backwards(self, orm):
        
        # Adding model 'DoorgenProfile'
        db.create_table('doorsadmin_doorgenprofile', (
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('settings', self.gf('django.db.models.fields.TextField')(default='')),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50)),
            ('dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('doorsadmin', ['DoorgenProfile'])

        # Adding field 'Doorway.doorgenProfile'
        db.add_column('doorsadmin_doorway', 'doorgenProfile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.DoorgenProfile'], null=True), keep_default=False)

        # Adding field 'Net.doorgenProfile'
        db.add_column('doorsadmin_net', 'doorgenProfile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.DoorgenProfile'], null=True), keep_default=False)


    models = {
        'doorsadmin.agent': {
            'Meta': {'object_name': 'Agent'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'currentTask': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateLastPing': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '3', 'null': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'doorsadmin.customquery': {
            'Meta': {'object_name': 'CustomQuery'},
            'database': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'default': "'localhost'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'sql': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'user': ('django.db.models.fields.CharField', [], {'default': "'admin'", 'max_length': '50'})
        },
        'doorsadmin.domain': {
            'Meta': {'object_name': 'Domain'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateExpires': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 8, 18)', 'null': 'True', 'blank': 'True'}),
            'dateRegistered': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Host']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipAddress': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.IPAddress']", 'null': 'True', 'blank': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'linkedDomains': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['doorsadmin.Domain']", 'null': 'True', 'blank': 'True'}),
            'makeSpam': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'maxDoorsCount': ('django.db.models.fields.IntegerField', [], {'default': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'nameServer1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'nameServer2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'net': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Net']", 'null': 'True', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True', 'blank': 'True'}),
            'registrator': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'useOwnDNS': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'doorsadmin.doorway': {
            'Meta': {'object_name': 'Doorway'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Agent']", 'null': 'True', 'blank': 'True'}),
            'analyticsId': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'cyclikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Domain']", 'null': 'True', 'blank': 'True'}),
            'domainFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywordsList': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'keywordsSet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.KeywordsSet']", 'null': 'True', 'blank': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'makeSpam': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'netLinksList': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'pagesCount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'piwikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'std'", 'max_length': '20'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'runTime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'spamLinksCount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'stateManaged': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Template']", 'null': 'True', 'blank': 'True'})
        },
        'doorsadmin.event': {
            'Meta': {'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'info'", 'max_length': '50', 'blank': 'True'})
        },
        'doorsadmin.host': {
            'Meta': {'object_name': 'Host'},
            'company': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'controlPanelServerId': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'controlPanelType': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '50', 'blank': 'True'}),
            'controlPanelUrl': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'costPerMonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'diskSpace': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ftpLogin': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'ftpPassword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'ftpPort': ('django.db.models.fields.IntegerField', [], {'default': '21', 'blank': 'True'}),
            'hostName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'rootDocumentTemplate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'traffic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'shared'", 'max_length': '50', 'blank': 'True'})
        },
        'doorsadmin.ipaddress': {
            'Meta': {'object_name': 'IPAddress'},
            'address': ('django.db.models.fields.IPAddressField', [], {'unique': 'True', 'max_length': '15'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Host']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
        },
        'doorsadmin.keywordsset': {
            'Meta': {'object_name': 'KeywordsSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'encoding': ('django.db.models.fields.CharField', [], {'default': "'cp1251'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywordsCount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
        },
        'doorsadmin.net': {
            'Meta': {'object_name': 'Net'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'analyticsId': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'cyclikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateEnd': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dateStart': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'doorsPerDay': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'doorsToday': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'generateNow': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywordsSet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.KeywordsSet']", 'null': 'True', 'blank': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'lastRun': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'makeSpam': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'maxPagesCount': ('django.db.models.fields.IntegerField', [], {'default': '900', 'null': 'True'}),
            'maxSpamLinksPercent': ('django.db.models.fields.FloatField', [], {'default': '5'}),
            'minPagesCount': ('django.db.models.fields.IntegerField', [], {'default': '500', 'null': 'True'}),
            'minSpamLinksPercent': ('django.db.models.fields.FloatField', [], {'default': '4'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'piwikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'settings': ('django.db.models.fields.TextField', [], {'default': "'#gen'", 'blank': 'True'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Template']", 'null': 'True', 'blank': 'True'})
        },
        'doorsadmin.niche': {
            'Meta': {'object_name': 'Niche'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'analyticsId': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'cyclikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'piwikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'stopwordsList': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'tdsSchemes': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'doorsadmin.snippetsset': {
            'Meta': {'object_name': 'SnippetsSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Agent']", 'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateLastParsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True'}),
            'keywordsCount': ('django.db.models.fields.IntegerField', [], {'default': '500', 'null': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFile': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'phrasesCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'std'", 'max_length': '20'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'runTime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'stateManaged': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
        },
        'doorsadmin.spamlink': {
            'Meta': {'object_name': 'SpamLink'},
            'anchor': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'doorway': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Doorway']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'makeSpam': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'spamTask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.SpamTask']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'})
        },
        'doorsadmin.spamtask': {
            'Meta': {'object_name': 'SpamTask'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Agent']", 'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'failsCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'halfSuccessCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'std'", 'max_length': '20'}),
            'profilesCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'runTime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'snippetsSet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.SnippetsSet']", 'null': 'True', 'blank': 'True'}),
            'stateManaged': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'successCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'xrumerBaseR': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.XrumerBaseR']", 'null': 'True'})
        },
        'doorsadmin.template': {
            'Meta': {'object_name': 'Template'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '50', 'blank': 'True'})
        },
        'doorsadmin.xrumerbaser': {
            'Meta': {'object_name': 'XrumerBaseR'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Agent']", 'null': 'True', 'blank': 'True'}),
            'baseNumber': ('django.db.models.fields.IntegerField', [], {'default': '48', 'unique': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'emailAddress': ('django.db.models.fields.CharField', [], {'default': "'niiokr2012@gmail.com'", 'max_length': '200'}),
            'emailLogin': ('django.db.models.fields.CharField', [], {'default': "'niiokr2012@gmail.com'", 'max_length': '200'}),
            'emailPassword': ('django.db.models.fields.CharField', [], {'default': "'kernel32'", 'max_length': '200'}),
            'emailPopServer': ('django.db.models.fields.CharField', [], {'default': "'pop.gmail.com'", 'max_length': '200'}),
            'failsCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'halfSuccessCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'linksCount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'nextSpamTaskDomainsCount': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'nickName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'std'", 'max_length': '20'}),
            'profilesCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'realName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'runTime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'snippetsSet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.SnippetsSet']", 'null': 'True', 'blank': 'True'}),
            'spamTaskDomainLinksMax': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'spamTaskDomainLinksMin': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'spamTaskDomainsMax': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'spamTaskDomainsMin': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'stateManaged': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'successCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'xrumerBaseRaw': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.XrumerBaseRaw']", 'null': 'True'})
        },
        'doorsadmin.xrumerbaseraw': {
            'Meta': {'object_name': 'XrumerBaseRaw'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'baseNumber': ('django.db.models.fields.IntegerField', [], {'default': '48', 'unique': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'linksCount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
        }
    }

    complete_apps = ['doorsadmin']
