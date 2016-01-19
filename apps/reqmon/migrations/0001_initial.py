# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Requests'
        db.delete_table(u'reqmon_requests')

        # Adding model 'Requests'
        db.create_table(u'reqmon_requests', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'reqmon', ['Requests'])


    def backwards(self, orm):
        # Deleting model 'Requests'
        db.delete_table(u'reqmon_requests')


    models = {
        u'reqmon.requests': {
            'Meta': {'object_name': 'Requests'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['reqmon']