from south.db import db
from django.db import models
from kanboard.models import *

class Migration:

    def forwards(self, orm):
        db.rename_column('kanboard_phase', 'type', 'status')
    
    def backwards(self, orm):
        db.rename_column('kanboard_phase', 'status', 'type')
    
    models = {
        'kanboard.board': {
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'kanboard.card': {
            'backlogged_at': ('django.db.models.fields.DateTimeField', [], {}),
            'blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'blocked_because': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'board': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards'", 'to': "orm['kanboard.Board']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'done_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards'", 'to': "orm['kanboard.Phase']"}),
            'ready': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'kanboard.phase': {
            'board': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'phases'", 'to': "orm['kanboard.Board']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'progress'", 'max_length': '25'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'kanboard.phaselog': {
            'Meta': {'unique_together': "(('phase', 'date'),)"},
            'count': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'to': "orm['kanboard.Phase']"})
        }
    }
    
    complete_apps = ['kanboard']
