import random
from django.test import TestCase

from kanboard.models import Board, Card, Phase

class KanboardTestCase(TestCase):
    def random_int(self):
        return random.randint(1, 1000)

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

    def create_card(self, save=True, **kwargs):
        if not kwargs:
            index = self.random_int()
            phase = self.create_phase()
            kwargs = {
                'title': 'Card %s' % index,
                'phase': phase,
                'order': 0,
            }
        c = self.create_object(Card, save, kwargs)
        if save:
            self.assert_(c.title)
            self.assert_(c.phase)
            self.assertNotEqual(None, c.order) #Because order can be 0
        return c

    def create_phase(self, save=True, **kwargs):
        if not kwargs:
            index = self.random_int()
            board = self.create_board()
            kwargs = {
                'title': 'Phase %s' % index,
                'board': board,
                'order': 0,
            }
        p = self.create_object(Phase, save, kwargs)
        if save:
            self.assert_(p.title)
            self.assert_(p.board)
            self.assertNotEqual(None, p.order)
        return p

    def create_object(self, klass, save=True, kwargs={}):
        o = klass(**kwargs) 
        if save:
            o.save()
            self.assert_(o.id, "Unable to save %s" % o)
        return o


class KanboardTests(KanboardTestCase):
    def setUp(self):
        self.board = self.create_board()

    def test_create(self):
        """
        Ensure that our convenience methods are actually working.
        """
        b = self.create_board()
        self.assert_(b.id)

        c = self.create_card()
        self.assert_(c.id)

        p = self.create_phase()
        self.assert_(p.id)

    def test_board_auto_phases(self):
        """
        A board, when created, should automatically have
        backlog, progress, done, and archive phases created as defaults.
        """
        b = self.create_board()
        self.assertEqual(4, len(b.phases.all()))

        self.assert_(b.backlog)
        self.assert_(b.done)
        self.assert_(b.archive)
