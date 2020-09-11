from django.test import TestCase

from ..factories import UserFactory


class UserTestCase(TestCase):

    @classmethod
    def setUp(cls):
        """Create new factory user."""
        cls.user = UserFactory.create()

    def test_first_name(self):
        """Check exists user's first name."""
        self.assertTrue(hasattr(self.user, 'first_name'))
