from django.test import TestCase

from kanboard.models import Card

class KanboardTests(TestCase):
    def test_environment(self):
        """Just make sure everything is set up correctly."""
        self.assert_(True)
