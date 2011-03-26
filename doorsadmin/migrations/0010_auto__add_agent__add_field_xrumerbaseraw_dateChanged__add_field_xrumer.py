# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Agent'
        db.create_table('doorsadmin_agent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('currentTask', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('lastPing', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('doorsadmin', ['Agent'])

        # Adding field 'XrumerBaseRaw.dateChanged'
        db.add_column('doorsadmin_xrumerbaseraw', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'XrumerBaseRaw.agent'
        db.add_column('doorsadmin_xrumerbaseraw', 'agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Agent'], null=True, blank=True), keep_default=False)

        # Adding field 'XrumerBaseR.dateChanged'
        db.add_column('doorsadmin_xrumerbaser', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'KeywordsSet.dateChanged'
        db.add_column('doorsadmin_keywordsset', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Deleting field 'Doorway.stateDoorway'
        db.delete_column('doorsadmin_doorway', 'stateDoorway')

        # Adding field 'Doorway.dateChanged'
        db.add_column('doorsadmin_doorway', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'Doorway.agent'
        db.add_column('doorsadmin_doorway', 'agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Agent'], null=True, blank=True), keep_default=False)

        # Adding field 'Server.dateChanged'
        db.add_column('doorsadmin_server', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'Server.costPerMonth'
        db.add_column('doorsadmin_server', 'costPerMonth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Server.diskSpace'
        db.add_column('doorsadmin_server', 'diskSpace', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Server.rootDocumentTemplate'
        db.add_column('doorsadmin_server', 'rootDocumentTemplate', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'IPAddress.dateChanged'
        db.add_column('doorsadmin_ipaddress', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'Net.dateChanged'
        db.add_column('doorsadmin_net', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'SnippetsSet.dateChanged'
        db.add_column('doorsadmin_snippetsset', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'SnippetsSet.agent'
        db.add_column('doorsadmin_snippetsset', 'agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Agent'], null=True, blank=True), keep_default=False)

        # Adding field 'FTPAccount.dateChanged'
        db.add_column('doorsadmin_ftpaccount', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'Template.dateChanged'
        db.add_column('doorsadmin_template', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'DoorwayTask.dateChanged'
        db.add_column('doorsadmin_doorwaytask', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Deleting field 'SpamTask.stateSpamTask'
        db.delete_column('doorsadmin_spamtask', 'stateSpamTask')

        # Adding field 'SpamTask.dateChanged'
        db.add_column('doorsadmin_spamtask', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'SpamTask.agent'
        db.add_column('doorsadmin_spamtask', 'agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Agent'], null=True, blank=True), keep_default=False)

        # Adding field 'XrumerProject.dateChanged'
        db.add_column('doorsadmin_xrumerproject', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'Niche.dateChanged'
        db.add_column('doorsadmin_niche', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'Niche.tdsSchemes'
        db.add_column('doorsadmin_niche', 'tdsSchemes', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'Domain.dateChanged'
        db.add_column('doorsadmin_domain', 'dateChanged', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True), keep_default=False)

        # Adding field 'Domain.registrator'
        db.add_column('doorsadmin_domain', 'registrator', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Agent'
        db.delete_table('doorsadmin_agent')

        # Deleting field 'XrumerBaseRaw.dateChanged'
        db.delete_column('doorsadmin_xrumerbaseraw', 'dateChanged')

        # Deleting field 'XrumerBaseRaw.agent'
        db.delete_column('doorsadmin_xrumerbaseraw', 'agent_id')

        # Deleting field 'XrumerBaseR.dateChanged'
        db.delete_column('doorsadmin_xrumerbaser', 'dateChanged')

        # Deleting field 'KeywordsSet.dateChanged'
        db.delete_column('doorsadmin_keywordsset', 'dateChanged')

        # Adding field 'Doorway.stateDoorway'
        db.add_column('doorsadmin_doorway', 'stateDoorway', self.gf('django.db.models.fields.CharField')(default='queue', max_length=50), keep_default=False)

        # Deleting field 'Doorway.dateChanged'
        db.delete_column('doorsadmin_doorway', 'dateChanged')

        # Deleting field 'Doorway.agent'
        db.delete_column('doorsadmin_doorway', 'agent_id')

        # Deleting field 'Server.dateChanged'
        db.delete_column('doorsadmin_server', 'dateChanged')

        # Deleting field 'Server.costPerMonth'
        db.delete_column('doorsadmin_server', 'costPerMonth')

        # Deleting field 'Server.diskSpace'
        db.delete_column('doorsadmin_server', 'diskSpace')

        # Deleting field 'Server.rootDocumentTemplate'
        db.delete_column('doorsadmin_server', 'rootDocumentTemplate')

        # Deleting field 'IPAddress.dateChanged'
        db.delete_column('doorsadmin_ipaddress', 'dateChanged')

        # Deleting field 'Net.dateChanged'
        db.delete_column('doorsadmin_net', 'dateChanged')

        # Deleting field 'SnippetsSet.dateChanged'
        db.delete_column('doorsadmin_snippetsset', 'dateChanged')

        # Deleting field 'SnippetsSet.agent'
        db.delete_column('doorsadmin_snippetsset', 'agent_id')

        # Deleting field 'FTPAccount.dateChanged'
        db.delete_column('doorsadmin_ftpaccount', 'dateChanged')

        # Deleting field 'Template.dateChanged'
        db.delete_column('doorsadmin_template', 'dateChanged')

        # Deleting field 'DoorwayTask.dateChanged'
        db.delete_column('doorsadmin_doorwaytask', 'dateChanged')

        # Adding field 'SpamTask.stateSpamTask'
        db.add_column('doorsadmin_spamtask', 'stateSpamTask', self.gf('django.db.models.fields.CharField')(default='ready', max_length=50), keep_default=False)

        # Deleting field 'SpamTask.dateChanged'
        db.delete_column('doorsadmin_spamtask', 'dateChanged')

        # Deleting field 'SpamTask.agent'
        db.delete_column('doorsadmin_spamtask', 'agent_id')

        # Deleting field 'XrumerProject.dateChanged'
        db.delete_column('doorsadmin_xrumerproject', 'dateChanged')

        # Deleting field 'Niche.dateChanged'
        db.delete_column('doorsadmin_niche', 'dateChanged')

        # Deleting field 'Niche.tdsSchemes'
        db.delete_column('doorsadmin_niche', 'tdsSchemes')

        # Deleting field 'Domain.dateChanged'
        db.delete_column('doorsadmin_domain', 'dateChanged')

        # Deleting field 'Domain.registrator'
        db.delete_column('doorsadmin_domain', 'registrator')


    models = {
        'doorsadmin.agent': {
            'Meta': {'object_name': 'Agent'},
            'currentTask': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastPing': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'doorsadmin.domain': {
            'Meta': {'object_name': 'Domain'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateExpires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dateRegistered': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'maxDoorsCount': ('django.db.models.fields.IntegerField', [], {'default': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nameServer1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'nameServer2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True', 'blank': 'True'}),
            'registrator': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Server']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.doorway': {
            'Meta': {'object_name': 'Doorway'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Agent']", 'null': 'True', 'blank': 'True'}),
            'allLinksList': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'analyticsId': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'cyclikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Domain']", 'null': 'True'}),
            'domainFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'doorwayTask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.DoorwayTask']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywordsList': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'keywordsSet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.KeywordsSet']", 'null': 'True', 'blank': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'net': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Net']", 'null': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'pagesCount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'piwikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'spamLinksList': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Template']", 'null': 'True', 'blank': 'True'})
        },
        'doorsadmin.doorwaytask': {
            'Meta': {'object_name': 'DoorwayTask'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'doorsPerDay': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'net': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Net']", 'null': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'pagesCountFrom': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pagesCountTo': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Template']", 'null': 'True', 'blank': 'True'})
        },
        'doorsadmin.ftpaccount': {
            'Meta': {'object_name': 'FTPAccount'},
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '21'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'remoteFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'server': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['doorsadmin.Server']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.ipaddress': {
            'Meta': {'object_name': 'IPAddress'},
            'address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['doorsadmin.Domain']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Server']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.keywordsset': {
            'Meta': {'object_name': 'KeywordsSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keysCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.net': {
            'Meta': {'object_name': 'Net'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'analyticsId': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'cyclikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'piwikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.niche': {
            'Meta': {'object_name': 'Niche'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'analyticsId': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'cyclikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'piwikId': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'}),
            'tdsSchemes': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'doorsadmin.server': {
            'Meta': {'object_name': 'Server'},
            'company': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'costPerMonth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'diskSpace': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hostName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'rootDocumentTemplate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.snippetsset': {
            'Meta': {'object_name': 'SnippetsSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Agent']", 'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateLastParsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFile': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'phraseCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
        },
        'doorsadmin.spamtask': {
            'Meta': {'object_name': 'SpamTask'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Agent']", 'null': 'True', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'doorways': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['doorsadmin.Doorway']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'spamLinksList': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'spamText': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'xrumerBaseR': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.XrumerBaseR']", 'null': 'True', 'blank': 'True'})
        },
        'doorsadmin.template': {
            'Meta': {'object_name': 'Template'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.xrumerbaser': {
            'Meta': {'object_name': 'XrumerBaseR'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'baseNumber': ('django.db.models.fields.IntegerField', [], {}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'}),
            'xrumerBaseRaw': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.XrumerBaseRaw']", 'null': 'True'})
        },
        'doorsadmin.xrumerbaseraw': {
            'Meta': {'object_name': 'XrumerBaseRaw'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Agent']", 'null': 'True', 'blank': 'True'}),
            'baseNumber': ('django.db.models.fields.IntegerField', [], {}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
        },
        'doorsadmin.xrumerproject': {
            'Meta': {'object_name': 'XrumerProject'},
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFile': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'spamTask': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['doorsadmin.SpamTask']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'}),
            'xrumerBaseR': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['doorsadmin.XrumerBaseR']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['doorsadmin']
