# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Blog'
        db.create_table('blogsadmin_blog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('indexCount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('indexCountDate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('backLinksCount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('backLinksCountDate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('bulkAddBlogs', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('blogsadmin', ['Blog'])

        # Adding model 'Position'
        db.create_table('blogsadmin_position', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blogsadmin.Blog'])),
            ('keyword', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('googlePosition', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('googleMaxPosition', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('googleExtendedInfo', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('yahooPosition', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yahooMaxPosition', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yahooExtendedInfo', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('bingPosition', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('bingMaxPosition', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('bingExtendedInfo', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('bulkAddKeywords', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('lastChecked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('blogsadmin', ['Position'])


    def backwards(self, orm):
        
        # Deleting model 'Blog'
        db.delete_table('blogsadmin_blog')

        # Deleting model 'Position'
        db.delete_table('blogsadmin_position')


    models = {
        'blogsadmin.blog': {
            'Meta': {'object_name': 'Blog'},
            'backLinksCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'backLinksCountDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'bulkAddBlogs': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indexCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'indexCountDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'blogsadmin.position': {
            'Meta': {'object_name': 'Position'},
            'bingExtendedInfo': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'bingMaxPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bingPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blogsadmin.Blog']"}),
            'bulkAddKeywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'googleExtendedInfo': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'googleMaxPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'googlePosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'lastChecked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'yahooExtendedInfo': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'yahooMaxPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yahooPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['blogsadmin']
