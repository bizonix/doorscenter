# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Niche'
        db.create_table('doorsadmin_niche', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('analyticsId', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('piwikId', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('cyclikId', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('doorsadmin', ['Niche'])

        # Adding model 'Server'
        db.create_table('doorsadmin_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('company', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('hostName', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
        ))
        db.send_create_signal('doorsadmin', ['Server'])

        # Adding model 'Domain'
        db.create_table('doorsadmin_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Niche'], null=True)),
            ('dateRegistered', self.gf('django.db.models.fields.DateField')(null=True)),
            ('dateExpires', self.gf('django.db.models.fields.DateField')(null=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Server'], null=True)),
            ('nameServer1', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('nameServer2', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('maxDoorsCount', self.gf('django.db.models.fields.IntegerField')(default=25)),
        ))
        db.send_create_signal('doorsadmin', ['Domain'])

        # Adding model 'IPAddress'
        db.create_table('doorsadmin_ipaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Server'], null=True)),
            ('domain', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['doorsadmin.Domain'], unique=True, null=True)),
        ))
        db.send_create_signal('doorsadmin', ['IPAddress'])

        # Adding model 'FTPAccount'
        db.create_table('doorsadmin_ftpaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('server', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['doorsadmin.Server'], unique=True, null=True)),
            ('login', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('password', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('remoteFolder', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('port', self.gf('django.db.models.fields.IntegerField')(default=21)),
        ))
        db.send_create_signal('doorsadmin', ['FTPAccount'])

        # Adding model 'Template'
        db.create_table('doorsadmin_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Niche'], null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('localFolder', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
        ))
        db.send_create_signal('doorsadmin', ['Template'])

        # Adding model 'Net'
        db.create_table('doorsadmin_net', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('analyticsId', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('piwikId', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('cyclikId', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('doorsadmin', ['Net'])

        # Adding model 'KeywordsSet'
        db.create_table('doorsadmin_keywordsset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Niche'], null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('localFolder', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('keysCount', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('doorsadmin', ['KeywordsSet'])

        # Adding model 'DoorwayTask'
        db.create_table('doorsadmin_doorwaytask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('net', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Net'], null=True)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Niche'], null=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Template'], null=True)),
            ('doorsQuantityPerDay', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('pagesCountFrom', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('pagesCountTo', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('doorsadmin', ['DoorwayTask'])

        # Adding model 'Doorway'
        db.create_table('doorsadmin_doorway', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('analyticsId', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('piwikId', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('cyclikId', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('net', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Net'], null=True)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Niche'], null=True)),
            ('keywordsSet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.KeywordsSet'], null=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Template'], null=True)),
            ('pagesCount', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Domain'], null=True)),
            ('domainFolder', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('localFolder', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('doorwayTask', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.DoorwayTask'], null=True)),
            ('stateDoorway', self.gf('django.db.models.fields.CharField')(default='queue', max_length=50)),
            ('keywordsList', self.gf('django.db.models.fields.TextField')(default='')),
            ('spamLinksList', self.gf('django.db.models.fields.TextField')(default='')),
            ('allLinksList', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('doorsadmin', ['Doorway'])

        # Adding model 'XrumerProject'
        db.create_table('doorsadmin_xrumerproject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('localFile', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('doorsadmin', ['XrumerProject'])

        # Adding model 'XrumerBaseRaw'
        db.create_table('doorsadmin_xrumerbaseraw', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('baseNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('localFile', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('doorsadmin', ['XrumerBaseRaw'])

        # Adding model 'XrumerBaseR'
        db.create_table('doorsadmin_xrumerbaser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('baseNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('localFile', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Niche'], null=True)),
            ('xrumerProject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.XrumerProject'], null=True)),
        ))
        db.send_create_signal('doorsadmin', ['XrumerBaseR'])

        # Adding model 'SpamTask'
        db.create_table('doorsadmin_spamtask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Niche'], null=True)),
            ('xrumerBaseR', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.XrumerBaseR'], null=True)),
            ('xrumerProject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.XrumerProject'], null=True)),
            ('spamLinksList', self.gf('django.db.models.fields.TextField')(default='')),
            ('text', self.gf('django.db.models.fields.TextField')(default='')),
            ('stateSpamTask', self.gf('django.db.models.fields.CharField')(default='ready', max_length=50)),
        ))
        db.send_create_signal('doorsadmin', ['SpamTask'])

        # Adding M2M table for field doorways on 'SpamTask'
        db.create_table('doorsadmin_spamtask_doorways', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('spamtask', models.ForeignKey(orm['doorsadmin.spamtask'], null=False)),
            ('doorway', models.ForeignKey(orm['doorsadmin.doorway'], null=False))
        ))
        db.create_unique('doorsadmin_spamtask_doorways', ['spamtask_id', 'doorway_id'])

        # Adding model 'SnippetsSet'
        db.create_table('doorsadmin_snippetsset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(default='')),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=50)),
            ('lastError', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('niche', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['doorsadmin.Niche'], null=True)),
            ('localFile', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('dateLastParsed', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('phraseCount', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('doorsadmin', ['SnippetsSet'])


    def backwards(self, orm):
        
        # Deleting model 'Niche'
        db.delete_table('doorsadmin_niche')

        # Deleting model 'Server'
        db.delete_table('doorsadmin_server')

        # Deleting model 'Domain'
        db.delete_table('doorsadmin_domain')

        # Deleting model 'IPAddress'
        db.delete_table('doorsadmin_ipaddress')

        # Deleting model 'FTPAccount'
        db.delete_table('doorsadmin_ftpaccount')

        # Deleting model 'Template'
        db.delete_table('doorsadmin_template')

        # Deleting model 'Net'
        db.delete_table('doorsadmin_net')

        # Deleting model 'KeywordsSet'
        db.delete_table('doorsadmin_keywordsset')

        # Deleting model 'DoorwayTask'
        db.delete_table('doorsadmin_doorwaytask')

        # Deleting model 'Doorway'
        db.delete_table('doorsadmin_doorway')

        # Deleting model 'XrumerProject'
        db.delete_table('doorsadmin_xrumerproject')

        # Deleting model 'XrumerBaseRaw'
        db.delete_table('doorsadmin_xrumerbaseraw')

        # Deleting model 'XrumerBaseR'
        db.delete_table('doorsadmin_xrumerbaser')

        # Deleting model 'SpamTask'
        db.delete_table('doorsadmin_spamtask')

        # Removing M2M table for field doorways on 'SpamTask'
        db.delete_table('doorsadmin_spamtask_doorways')

        # Deleting model 'SnippetsSet'
        db.delete_table('doorsadmin_snippetsset')


    models = {
        'doorsadmin.domain': {
            'Meta': {'object_name': 'Domain'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateExpires': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'dateRegistered': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'maxDoorsCount': ('django.db.models.fields.IntegerField', [], {'default': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nameServer1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'nameServer2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Server']", 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.doorway': {
            'Meta': {'object_name': 'Doorway'},
            'allLinksList': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'analyticsId': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'cyclikId': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Domain']", 'null': 'True'}),
            'domainFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'doorwayTask': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.DoorwayTask']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywordsList': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'keywordsSet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.KeywordsSet']", 'null': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'localFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'net': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Net']", 'null': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'pagesCount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'piwikId': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'spamLinksList': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'}),
            'stateDoorway': ('django.db.models.fields.CharField', [], {'default': "'queue'", 'max_length': '50'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Template']", 'null': 'True'})
        },
        'doorsadmin.doorwaytask': {
            'Meta': {'object_name': 'DoorwayTask'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'doorsQuantityPerDay': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'net': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Net']", 'null': 'True'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'pagesCountFrom': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'pagesCountTo': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Template']", 'null': 'True'})
        },
        'doorsadmin.ftpaccount': {
            'Meta': {'object_name': 'FTPAccount'},
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'login': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '21'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'remoteFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'server': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['doorsadmin.Server']", 'unique': 'True', 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.ipaddress': {
            'Meta': {'object_name': 'IPAddress'},
            'address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['doorsadmin.Domain']", 'unique': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Server']", 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.keywordsset': {
            'Meta': {'object_name': 'KeywordsSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keysCount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'localFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.net': {
            'Meta': {'object_name': 'Net'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'analyticsId': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'cyclikId': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'piwikId': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.niche': {
            'Meta': {'object_name': 'Niche'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'analyticsId': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'cyclikId': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'piwikId': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.server': {
            'Meta': {'object_name': 'Server'},
            'company': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'hostName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.snippetsset': {
            'Meta': {'object_name': 'SnippetsSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dateLastParsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'localFile': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'phraseCount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.spamtask': {
            'Meta': {'object_name': 'SpamTask'},
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'doorways': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['doorsadmin.Doorway']", 'null': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'spamLinksList': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'}),
            'stateSpamTask': ('django.db.models.fields.CharField', [], {'default': "'ready'", 'max_length': '50'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'xrumerBaseR': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.XrumerBaseR']", 'null': 'True'}),
            'xrumerProject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.XrumerProject']", 'null': 'True'})
        },
        'doorsadmin.template': {
            'Meta': {'object_name': 'Template'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'localFolder': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.xrumerbaser': {
            'Meta': {'object_name': 'XrumerBaseR'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'baseNumber': ('django.db.models.fields.IntegerField', [], {}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'localFile': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'niche': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.Niche']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'}),
            'xrumerProject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['doorsadmin.XrumerProject']", 'null': 'True'})
        },
        'doorsadmin.xrumerbaseraw': {
            'Meta': {'object_name': 'XrumerBaseRaw'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'baseNumber': ('django.db.models.fields.IntegerField', [], {}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'localFile': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        },
        'doorsadmin.xrumerproject': {
            'Meta': {'object_name': 'XrumerProject'},
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastError': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'localFile': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'remarks': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '50'})
        }
    }

    complete_apps = ['doorsadmin']
