import random
from django.test import TestCase

from kanboard.models import Board, Card, Phase

class KanboardTestCase(TestCase):
    def random_int(self):
        return random.randint(1, 100)

    def create_board(self, save=True, **kwargs):
        if not kwargs:
            index = self.random_int()
            kwargs = {
                'title': 'Test Board %s' % index,
                'slug': 'test-board-%s' % index,
            }
                
        b = self.create_object(Board, save, kwargs)
        if save:
            self.assert_(b.title)
            self.assert_(b.slug)
        return b

    def create_object(self, klass, save=True, kwargs={}):
        o = klass(**kwargs) 
        if save:
            o.save()
            self.assert_(o.id, "Unable to save %s" % o)
        return o

class KanboardTests(KanboardTestCase):
    def test_create(self):
        b = self.create_board()
        self.assert_(b.id)

