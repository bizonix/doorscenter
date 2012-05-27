# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Position.yahooMaxPositionDate'
        db.alter_column('blogsadmin_position', 'yahooMaxPositionDate', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Position.googleMaxPositionDate'
        db.alter_column('blogsadmin_position', 'googleMaxPositionDate', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Position.bingMaxPositionDate'
        db.alter_column('blogsadmin_position', 'bingMaxPositionDate', self.gf('django.db.models.fields.DateTimeField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'Position.yahooMaxPositionDate'
        db.alter_column('blogsadmin_position', 'yahooMaxPositionDate', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Position.googleMaxPositionDate'
        db.alter_column('blogsadmin_position', 'googleMaxPositionDate', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Position.bingMaxPositionDate'
        db.alter_column('blogsadmin_position', 'bingMaxPositionDate', self.gf('django.db.models.fields.DateField')(null=True))


    models = {
        'blogsadmin.blog': {
            'Meta': {'object_name': 'Blog'},
            'backLinksCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bulkAddBlogs': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indexCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lastChecked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'blogsadmin.position': {
            'Meta': {'object_name': 'Position'},
            'bingExtendedInfo': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'bingMaxPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bingMaxPositionDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'bingPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blogsadmin.Blog']"}),
            'bulkAddKeywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'googleExtendedInfo': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'googleMaxPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'googleMaxPositionDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'googlePosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'lastChecked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'yahooExtendedInfo': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'yahooMaxPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yahooMaxPositionDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'yahooPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['blogsadmin']
