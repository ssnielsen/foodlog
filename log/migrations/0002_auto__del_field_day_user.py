# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Day.user'
        db.delete_column(u'log_day', 'user_id')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Day.user'
        raise RuntimeError("Cannot reverse this migration. 'Day.user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Day.user'
        db.add_column(u'log_day', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                      keep_default=False)


    models = {
        u'log.day': {
            'Meta': {'object_name': 'Day'},
            'day': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_cal': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'log.food': {
            'Meta': {'object_name': 'Food'},
            'carbo': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'}),
            'energy': ('django.db.models.fields.IntegerField', [], {}),
            'fat': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protein': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'log.serving': {
            'Meta': {'ordering': "['meal']", 'object_name': 'Serving'},
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['log.Day']"}),
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['log.Food']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['log']