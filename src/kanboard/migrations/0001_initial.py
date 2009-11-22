
from south.db import db
from django.db import models
from kanboard.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'PhaseLog'
        db.create_table('kanboard_phaselog', (
            ('id', orm['kanboard.PhaseLog:id']),
            ('phase', orm['kanboard.PhaseLog:phase']),
            ('count', orm['kanboard.PhaseLog:count']),
            ('date', orm['kanboard.PhaseLog:date']),
        ))
        db.send_create_signal('kanboard', ['PhaseLog'])
        
        # Adding model 'Board'
        db.create_table('kanboard_board', (
            ('id', orm['kanboard.Board:id']),
            ('title', orm['kanboard.Board:title']),
            ('slug', orm['kanboard.Board:slug']),
            ('description', orm['kanboard.Board:description']),
        ))
        db.send_create_signal('kanboard', ['Board'])
        
        # Adding model 'Card'
        db.create_table('kanboard_card', (
            ('id', orm['kanboard.Card:id']),
            ('title', orm['kanboard.Card:title']),
            ('board', orm['kanboard.Card:board']),
            ('phase', orm['kanboard.Card:phase']),
            ('order', orm['kanboard.Card:order']),
            ('backlogged_at', orm['kanboard.Card:backlogged_at']),
            ('started_at', orm['kanboard.Card:started_at']),
            ('done_at', orm['kanboard.Card:done_at']),
            ('description', orm['kanboard.Card:description']),
            ('size', orm['kanboard.Card:size']),
            ('color', orm['kanboard.Card:color']),
            ('ready', orm['kanboard.Card:ready']),
            ('blocked', orm['kanboard.Card:blocked']),
            ('blocked_because', orm['kanboard.Card:blocked_because']),
        ))
        db.send_create_signal('kanboard', ['Card'])
        
        # Adding model 'Phase'
        db.create_table('kanboard_phase', (
            ('id', orm['kanboard.Phase:id']),
            ('title', orm['kanboard.Phase:title']),
            ('board', orm['kanboard.Phase:board']),
            ('order', orm['kanboard.Phase:order']),
            ('type', orm['kanboard.Phase:type']),
            ('description', orm['kanboard.Phase:description']),
            ('limit', orm['kanboard.Phase:limit']),
        ))
        db.send_create_signal('kanboard', ['Phase'])
        
        # Creating unique_together for [phase, date] on PhaseLog.
        db.create_unique('kanboard_phaselog', ['phase_id', 'date'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [phase, date] on PhaseLog.
        db.delete_unique('kanboard_phaselog', ['phase_id', 'date'])
        
        # Deleting model 'PhaseLog'
        db.delete_table('kanboard_phaselog')
        
        # Deleting model 'Board'
        db.delete_table('kanboard_board')
        
        # Deleting model 'Card'
        db.delete_table('kanboard_card')
        
        # Deleting model 'Phase'
        db.delete_table('kanboard_phase')
        
    
    
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'progress'", 'max_length': '25'})
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
