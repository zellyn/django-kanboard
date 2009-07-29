# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.management.base import LabelCommand

from kanboard.models import Board, Card, Phase

class Command(LabelCommand):
    def handle_label(self, label, **options):
        if label == 'createdata':
            self.create_data()
            return
        raise Exception("kanboard management command doesn\'t know about option: '%s'" % (label,))

    def create_data(self):
        Card.objects.all().delete()
        Phase.objects.all().delete()
        Board.objects.all().delete()

        b = Board.objects.create(
            title='Test Board', slug='test-board',
            description='A test kanban board')
        backlog, done, archive = b.phases.all()

        c1 = Card.objects.create(
            title='Snow White',
            description='A movie about Snow White. Animated, probably.',
            phase=backlog,
            order=1,
            backlogged_at=datetime.now(),
            )

        c2 = Card.objects.create(
            title='The Little Mermaid',
            description='Another possible animated film.',
            phase=backlog,
            order=2,
            backlogged_at=datetime.now(),
            )

        c3 = Card.objects.create(
            title='Aladdin',
            description='Genie, flying carpet, etc.',
            phase=done,
            order=1,
            backlogged_at=datetime.now(),
            )

        c4 = Card.objects.create(
            title='Shrek',
            description='Big green guy, donkey, etc.',
            phase=archive,
            order=1,
            backlogged_at=datetime.now(),
            )

        c5 = Card.objects.create(
            title='Shrek 5',
            description="Because there's no such thing as “too many.”",
            phase=archive,
            order=2,
            backlogged_at=datetime.now(),
            )
