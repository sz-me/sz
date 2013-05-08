# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'core_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(max_length=2048)),
        ))
        db.send_create_signal(u'core', ['Category'])

        # Adding model 'Place'
        db.create_table(u'core_place', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=24, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('crossStreet', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('position', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('city_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('foursquare_icon_prefix', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('foursquare_icon_suffix', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Place'])

        # Adding model 'Stem'
        db.create_table(u'core_stem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stem', self.gf('sz.core.models.LowerCaseCharField')(unique=True, max_length=32, db_index=True)),
            ('language', self.gf('sz.core.models.LowerCaseCharField')(max_length=2, db_index=True)),
        ))
        db.send_create_signal(u'core', ['Stem'])

        # Adding unique constraint on 'Stem', fields ['stem', 'language']
        db.create_unique(u'core_stem', ['stem', 'language'])

        # Adding model 'Style'
        db.create_table(u'core_style', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Style'])

        # Adding model 'User'
        db.create_table(u'core_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=72, db_index=True)),
            ('style', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Style'], null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'core', ['User'])

        # Adding model 'Smile'
        db.create_table(u'core_smile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emotion', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('style', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Style'], null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Smile'])

        # Adding model 'Message'
        db.create_table(u'core_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=1024, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Place'])),
            ('photo', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100, blank=True)),
            ('smile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Smile'])),
        ))
        db.send_create_signal(u'core', ['Message'])

        # Adding M2M table for field categories on 'Message'
        db.create_table(u'core_message_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm[u'core.message'], null=False)),
            ('category', models.ForeignKey(orm[u'core.category'], null=False))
        ))
        db.create_unique(u'core_message_categories', ['message_id', 'category_id'])

        # Adding M2M table for field stems on 'Message'
        db.create_table(u'core_message_stems', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm[u'core.message'], null=False)),
            ('stem', models.ForeignKey(orm[u'core.stem'], null=False))
        ))
        db.create_unique(u'core_message_stems', ['message_id', 'stem_id'])

        # Adding model 'MessagePreview'
        db.create_table(u'core_messagepreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=1024, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.User'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Place'])),
            ('photo', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100, blank=True)),
            ('smile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Smile'])),
        ))
        db.send_create_signal(u'core', ['MessagePreview'])

        # Adding M2M table for field categories on 'MessagePreview'
        db.create_table(u'core_messagepreview_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('messagepreview', models.ForeignKey(orm[u'core.messagepreview'], null=False)),
            ('category', models.ForeignKey(orm[u'core.category'], null=False))
        ))
        db.create_unique(u'core_messagepreview_categories', ['messagepreview_id', 'category_id'])

        # Adding model 'CensorBox'
        db.create_table(u'core_censorbox', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message_preview', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.MessagePreview'])),
            ('x', self.gf('django.db.models.fields.FloatField')()),
            ('y', self.gf('django.db.models.fields.FloatField')()),
            ('r', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'core', ['CensorBox'])


    def backwards(self, orm):
        # Removing unique constraint on 'Stem', fields ['stem', 'language']
        db.delete_unique(u'core_stem', ['stem', 'language'])

        # Deleting model 'Category'
        db.delete_table(u'core_category')

        # Deleting model 'Place'
        db.delete_table(u'core_place')

        # Deleting model 'Stem'
        db.delete_table(u'core_stem')

        # Deleting model 'Style'
        db.delete_table(u'core_style')

        # Deleting model 'User'
        db.delete_table(u'core_user')

        # Deleting model 'Smile'
        db.delete_table(u'core_smile')

        # Deleting model 'Message'
        db.delete_table(u'core_message')

        # Removing M2M table for field categories on 'Message'
        db.delete_table('core_message_categories')

        # Removing M2M table for field stems on 'Message'
        db.delete_table('core_message_stems')

        # Deleting model 'MessagePreview'
        db.delete_table(u'core_messagepreview')

        # Removing M2M table for field categories on 'MessagePreview'
        db.delete_table('core_messagepreview_categories')

        # Deleting model 'CensorBox'
        db.delete_table(u'core_censorbox')


    models = {
        u'core.category': {
            'Meta': {'object_name': 'Category'},
            'alias': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        },
        u'core.censorbox': {
            'Meta': {'object_name': 'CensorBox'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_preview': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.MessagePreview']"}),
            'r': ('django.db.models.fields.FloatField', [], {}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.message': {
            'Meta': {'object_name': 'Message'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Category']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Place']"}),
            'smile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Smile']"}),
            'stems': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Stem']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']"})
        },
        u'core.messagepreview': {
            'Meta': {'object_name': 'MessagePreview'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Category']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Place']"}),
            'smile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Smile']"}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.User']"})
        },
        u'core.place': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Place'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'city_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'crossStreet': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'foursquare_icon_prefix': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'foursquare_icon_suffix': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'position': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        u'core.smile': {
            'Meta': {'object_name': 'Smile'},
            'emotion': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Style']", 'null': 'True', 'blank': 'True'})
        },
        u'core.stem': {
            'Meta': {'unique_together': "(('stem', 'language'),)", 'object_name': 'Stem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('sz.core.models.LowerCaseCharField', [], {'max_length': '2', 'db_index': 'True'}),
            'stem': ('sz.core.models.LowerCaseCharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'})
        },
        u'core.style': {
            'Meta': {'object_name': 'Style'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'core.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '72', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Style']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']