# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Agent.state'
        db.delete_column('doorsadmin_agent', 'state')

        # Adding field 'Agent.stateSimple'
        db.add_column('doorsadmin_agent', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'XrumerBaseRaw.state'
        db.delete_column('doorsadmin_xrumerbaseraw', 'state')

        # Adding field 'XrumerBaseRaw.stateSimple'
        db.add_column('doorsadmin_xrumerbaseraw', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Adding field 'XrumerBaseRaw.stateManaged'
        db.add_column('doorsadmin_xrumerbaseraw', 'stateManaged', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'XrumerBaseR.state'
        db.delete_column('doorsadmin_xrumerbaser', 'state')

        # Adding field 'XrumerBaseR.stateSimple'
        db.add_column('doorsadmin_xrumerbaser', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'KeywordsSet.state'
        db.delete_column('doorsadmin_keywordsset', 'state')

        # Adding field 'KeywordsSet.stateSimple'
        db.add_column('doorsadmin_keywordsset', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Doorway.state'
        db.delete_column('doorsadmin_doorway', 'state')

        # Adding field 'Doorway.stateSimple'
        db.add_column('doorsadmin_doorway', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Adding field 'Doorway.stateManaged'
        db.add_column('doorsadmin_doorway', 'stateManaged', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Server.state'
        db.delete_column('doorsadmin_server', 'state')

        # Adding field 'Server.stateSimple'
        db.add_column('doorsadmin_server', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'IPAddress.state'
        db.delete_column('doorsadmin_ipaddress', 'state')

        # Adding field 'IPAddress.stateSimple'
        db.add_column('doorsadmin_ipaddress', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Net.state'
        db.delete_column('doorsadmin_net', 'state')

        # Adding field 'Net.stateSimple'
        db.add_column('doorsadmin_net', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'SnippetsSet.state'
        db.delete_column('doorsadmin_snippetsset', 'state')

        # Adding field 'SnippetsSet.stateSimple'
        db.add_column('doorsadmin_snippetsset', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Adding field 'SnippetsSet.stateManaged'
        db.add_column('doorsadmin_snippetsset', 'stateManaged', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'FTPAccount.state'
        db.delete_column('doorsadmin_ftpaccount', 'state')

        # Adding field 'FTPAccount.stateSimple'
        db.add_column('doorsadmin_ftpaccount', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Domain.state'
        db.delete_column('doorsadmin_domain', 'state')

        # Adding field 'Domain.stateSimple'
        db.add_column('doorsadmin_domain', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'DoorwayTask.state'
        db.delete_column('doorsadmin_doorwaytask', 'state')

        # Adding field 'DoorwayTask.stateSimple'
        db.add_column('doorsadmin_doorwaytask', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'SpamTask.state'
        db.delete_column('doorsadmin_spamtask', 'state')

        # Adding field 'SpamTask.stateSimple'
        db.add_column('doorsadmin_spamtask', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Adding field 'SpamTask.stateManaged'
        db.add_column('doorsadmin_spamtask', 'stateManaged', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'XrumerProject.state'
        db.delete_column('doorsadmin_xrumerproject', 'state')

        # Adding field 'XrumerProject.stateSimple'
        db.add_column('doorsadmin_xrumerproject', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Niche.state'
        db.delete_column('doorsadmin_niche', 'state')

        # Adding field 'Niche.stateSimple'
        db.add_column('doorsadmin_niche', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Template.state'
        db.delete_column('doorsadmin_template', 'state')

        # Adding field 'Template.stateSimple'
        db.add_column('doorsadmin_template', 'stateSimple', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Agent.state'
        db.add_column('doorsadmin_agent', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Agent.stateSimple'
        db.delete_column('doorsadmin_agent', 'stateSimple')

        # Adding field 'XrumerBaseRaw.state'
        db.add_column('doorsadmin_xrumerbaseraw', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'XrumerBaseRaw.stateSimple'
        db.delete_column('doorsadmin_xrumerbaseraw', 'stateSimple')

        # Deleting field 'XrumerBaseRaw.stateManaged'
        db.delete_column('doorsadmin_xrumerbaseraw', 'stateManaged')

        # Adding field 'XrumerBaseR.state'
        db.add_column('doorsadmin_xrumerbaser', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'XrumerBaseR.stateSimple'
        db.delete_column('doorsadmin_xrumerbaser', 'stateSimple')

        # Adding field 'KeywordsSet.state'
        db.add_column('doorsadmin_keywordsset', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'KeywordsSet.stateSimple'
        db.delete_column('doorsadmin_keywordsset', 'stateSimple')

        # Adding field 'Doorway.state'
        db.add_column('doorsadmin_doorway', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Doorway.stateSimple'
        db.delete_column('doorsadmin_doorway', 'stateSimple')

        # Deleting field 'Doorway.stateManaged'
        db.delete_column('doorsadmin_doorway', 'stateManaged')

        # Adding field 'Server.state'
        db.add_column('doorsadmin_server', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Server.stateSimple'
        db.delete_column('doorsadmin_server', 'stateSimple')

        # Adding field 'IPAddress.state'
        db.add_column('doorsadmin_ipaddress', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'IPAddress.stateSimple'
        db.delete_column('doorsadmin_ipaddress', 'stateSimple')

        # Adding field 'Net.state'
        db.add_column('doorsadmin_net', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Net.stateSimple'
        db.delete_column('doorsadmin_net', 'stateSimple')

        # Adding field 'SnippetsSet.state'
        db.add_column('doorsadmin_snippetsset', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'SnippetsSet.stateSimple'
        db.delete_column('doorsadmin_snippetsset', 'stateSimple')

        # Deleting field 'SnippetsSet.stateManaged'
        db.delete_column('doorsadmin_snippetsset', 'stateManaged')

        # Adding field 'FTPAccount.state'
        db.add_column('doorsadmin_ftpaccount', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'FTPAccount.stateSimple'
        db.delete_column('doorsadmin_ftpaccount', 'stateSimple')

        # Adding field 'Domain.state'
        db.add_column('doorsadmin_domain', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Domain.stateSimple'
        db.delete_column('doorsadmin_domain', 'stateSimple')

        # Adding field 'DoorwayTask.state'
        db.add_column('doorsadmin_doorwaytask', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'DoorwayTask.stateSimple'
        db.delete_column('doorsadmin_doorwaytask', 'stateSimple')

        # Adding field 'SpamTask.state'
        db.add_column('doorsadmin_spamtask', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'SpamTask.stateSimple'
        db.delete_column('doorsadmin_spamtask', 'stateSimple')

        # Deleting field 'SpamTask.stateManaged'
        db.delete_column('doorsadmin_spamtask', 'stateManaged')

        # Adding field 'XrumerProject.state'
        db.add_column('doorsadmin_xrumerproject', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'XrumerProject.stateSimple'
        db.delete_column('doorsadmin_xrumerproject', 'stateSimple')

        # Adding field 'Niche.state'
        db.add_column('doorsadmin_niche', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Niche.stateSimple'
        db.delete_column('doorsadmin_niche', 'stateSimple')

        # Adding field 'Template.state'
        db.add_column('doorsadmin_template', 'state', self.gf('django.db.models.fields.CharField')(default='new', max_length=50), keep_default=False)

        # Deleting field 'Template.stateSimple'
        db.delete_column('doorsadmin_template', 'stateSimple')


    models = {
        'doorsadmin.agent': {
            'Meta': {'object_name': 'Agent'},
            'agentId': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'agentType': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'currentTask': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastChanged': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
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
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
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
            'stateManaged': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
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
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
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
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
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
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
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
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
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
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
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
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
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
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
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
            'stateManaged': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
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
            'stateManaged': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
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
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
        },
        'doorsadmin.xrumerbaser': {
            'Meta': {'object_name': 'XrumerBaseR'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'baseNumber': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'xrumerBaseRaw': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.XrumerBaseRaw']", 'null': 'True'})
        },
        'doorsadmin.xrumerbaseraw': {
            'Meta': {'object_name': 'XrumerBaseRaw'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Agent']", 'null': 'True', 'blank': 'True'}),
            'baseNumber': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateChanged': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'localFile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stateManaged': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'})
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
            'stateSimple': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '50'}),
            'xrumerBaseR': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['doorsadmin.XrumerBaseR']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['doorsadmin']
