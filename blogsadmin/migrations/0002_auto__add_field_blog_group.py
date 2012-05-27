# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Blog.group'
        db.add_column('blogsadmin_blog', 'group', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Blog.group'
        db.delete_column('blogsadmin_blog', 'group')


    models = {
        'blogsadmin.blog': {
            'Meta': {'object_name': 'Blog'},
            'backLinksCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'backLinksCountDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'bulkAddBlogs': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
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
