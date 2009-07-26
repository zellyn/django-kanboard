import datetime
import random

from django.test import TestCase

from kanboard.models import Board, Card, Phase, KanboardStats

class KanboardTestCase(TestCase):
    def setUp(self):
        self.board = self.create_board()

        self.backlog = self.board.get_backlog()
        self.ideation = self.create_phase(save=True, title="Ideation", order=1, board=self.board)
        self.design = self.create_phase(save=True, title="Design", order=2, board=self.board)
        self.dev = self.create_phase(save=True, title="Development", order=3, board=self.board)
        self.test = self.create_phase(save=True, title="Testing", order=4, board=self.board)
        self.deploy = self.create_phase(save=True, title="Deployment", order=5, board=self.board)
        self.done = self.board.get_done()
        self.archive = self.board.get_archive()
        
        super(KanboardTestCase, self).setUp()

    def random_int(self):
        return random.randint(1, 1000)

    def create_board(self, save=True, **kwargs):
        index = self.random_int()
        defaults = {
            'title': 'Test Board %s' % index,
            'slug': 'test-board-%s' % index,
        }
        defaults.update(kwargs)
        b = self.create_object(Board, save, defaults)
        if save:
            self.assert_(b.title)
            self.assert_(b.slug)
        return b

    def create_card(self, save=True, **kwargs):
        index = self.random_int()
        phase = self.create_phase()
        defaults = {
            'title': 'Card %s' % index,
            'phase': phase,
            'order': 0,
        }
        defaults.update(kwargs)
        c = self.create_object(Card, save, defaults)
        if save:
            self.assert_(c.title)
            self.assert_(c.phase)
            self.assertNotEqual(None, c.order) #Because order can be 0
        return c

    def create_phase(self, save=True, **kwargs):
        index = self.random_int()
        board = self.create_board()
        defaults = {
            'title': 'Phase %s' % index,
            'board': board,
            'order': 0,
        }
        defaults.update(kwargs)

        p = self.create_object(Phase, save, defaults)
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
        self.assertEqual(3, len(b.phases.all()))

        self.assert_(b.get_backlog())
        self.assert_(b.get_done())
        self.assert_(b.get_archive())

    def test_phase_ordering(self):
        """
        board.phases.all() should return them in order.
        """
        expected = [self.board.get_backlog(), self.ideation, self.design, self.dev, self.test, self.deploy, self.board.get_done(), self.board.get_archive()]
        actual = list(self.board.phases.all())
       
        from pprint import pformat
        msg = "%s\n%s" % (pformat(expected), pformat(actual))
        self.assertEqual(expected, actual, msg)

    def test_cards_ordering(self):
        """
        phase.cards.all() should return them in order.
        """
        backlog = self.board.get_backlog()

        common_args = dict(save=True, phase=backlog)
        card2 = self.create_card(order=2, **common_args)
        card1 = self.create_card(order=1, **common_args)
        card0 = self.create_card(order=0, **common_args)

        expected = [card0, card1, card2]
        actual = list(backlog.cards.all())

        self.assertEqual(expected, actual)
    
    def test_card_changing_phase(self):
        """
        card.change_phase(phase) should move the card to that phase.
        It should update card.started_at and card.done_at if appropriate.
        """
        card = self.create_card(phase=self.backlog)
        self.assert_(card.backlogged_at)

        card.change_phase(self.ideation)
        self.assert_(card.started_at)

        card.change_phase(self.design)
        card.change_phase(self.done)
        self.assert_(card.done_at)
        done_at = card.done_at

        card.change_phase(self.archive)
        self.assertEqual(done_at, card.done_at)

    def test_phase_change_with_datetime(self):
        """
        card.change_phase should accept an optional datetime argument.
        All applicable card timestamps should be updated to use
        that argument.
        """
        now = datetime.datetime.now()
        later = datetime.datetime.now() + datetime.timedelta(days=2)
        way_later = later + datetime.timedelta(days=7)

        card = self.create_card(phase=self.backlog, backlogged_at=now)
        self.assertEqual(card.backlogged_at, now)

        card.change_phase(self.design, change_at=later)
        self.assertEqual(card.started_at, later)

        card.change_phase(self.archive, change_at=way_later)
        self.assertEqual(card.done_at, way_later)

class StatsTests(KanboardTestCase):
    def setUp(self):
        super(StatsTests, self).setUp()
        self.stats = KanboardStats(board=self.board)

    def set_up_board(self, expected_counts, board=None):
        if board is None:
            board = self.board

        for phase_name, count in expected_counts.items():
            phase = Phase.objects.get(title=phase_name, board=self.board)
            for i in xrange(0, count+1):
                card =self.create_card()
                card.change_phase(phase) 

    def test_cumulative_flow(self):
        """
        cumulative_flow should return a dictionary-like object,
        each key is a Phase name and the value is the number of 
        objects that were in that phase on that day.

        Note: The done count should equal Done + Archive
        """
        expected = {
            u'Backlog': 5,
            u'Ideation': 2,
            u'Design': 7,
            u'Development': 3,
            u'Testing': 6,
            u'Deployment': 1,
            u'Done': 3,
        }
        self.set_up_board(expected)

        result = self.stats.cumulative_flow()

        self.assertEqual(expected, result)
