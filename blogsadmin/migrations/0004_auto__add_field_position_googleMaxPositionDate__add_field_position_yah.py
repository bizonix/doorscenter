# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Position.googleMaxPositionDate'
        db.add_column('blogsadmin_position', 'googleMaxPositionDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Position.yahooMaxPositionDate'
        db.add_column('blogsadmin_position', 'yahooMaxPositionDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Position.bingMaxPositionDate'
        db.add_column('blogsadmin_position', 'bingMaxPositionDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Blog.indexCountDate'
        db.delete_column('blogsadmin_blog', 'indexCountDate')

        # Deleting field 'Blog.backLinksCountDate'
        db.delete_column('blogsadmin_blog', 'backLinksCountDate')

        # Adding field 'Blog.lastChecked'
        db.add_column('blogsadmin_blog', 'lastChecked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Position.googleMaxPositionDate'
        db.delete_column('blogsadmin_position', 'googleMaxPositionDate')

        # Deleting field 'Position.yahooMaxPositionDate'
        db.delete_column('blogsadmin_position', 'yahooMaxPositionDate')

        # Deleting field 'Position.bingMaxPositionDate'
        db.delete_column('blogsadmin_position', 'bingMaxPositionDate')

        # Adding field 'Blog.indexCountDate'
        db.add_column('blogsadmin_blog', 'indexCountDate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Blog.backLinksCountDate'
        db.add_column('blogsadmin_blog', 'backLinksCountDate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Blog.lastChecked'
        db.delete_column('blogsadmin_blog', 'lastChecked')


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
            'bingMaxPositionDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bingPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blogsadmin.Blog']"}),
            'bulkAddKeywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'googleExtendedInfo': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'googleMaxPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'googleMaxPositionDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'googlePosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'lastChecked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'yahooExtendedInfo': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'yahooMaxPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yahooMaxPositionDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'yahooPosition': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['blogsadmin']
