from unittest.mock import MagicMock

from django.test import TestCase

from ..posts.factories import PostFactory
from ..users.factories import UserFactory
from .models import Reaction
from .views import ReactionCreate


class ReactionTestCase(TestCase):

    def setUp(self):
        """Create new post, user and ReactionView."""
        self.user = UserFactory()
        self.post = PostFactory()

        self.view = ReactionCreate()
        self.view.kwargs = {'pk': self.post.id}

        self.request = MagicMock()
        self.request.user = self.user

        self.view.request = self.request

    def test_reaction_add(self):
        """Test reaction creates"""
        reaction = Reaction.LIKE

        self.request.method = 'POST'
        self.request.POST = {'description': reaction}

        self.view.post(self.request, pk=self.post.id)

        self.assertTrue(self.user.reactions.all())
        self.assertTrue(self.post.reactions.all())
        self.assertEqual(
            self.user.reactions.all().first().description,
            reaction,
        )

    def test_reaction_single(self):
        """Test user can react only once by one emote"""
        reaction1 = Reaction.LIKE

        self.request.method = 'POST'
        self.request.POST = {'description': reaction1}
        self.view.post(self.request, pk=self.post.id)
        self.view.post(self.request, pk=self.post.id)

        self.assertEqual(self.post.reactions.count(), 1)
        self.assertEqual(
            self.post.reactions.all().first().description,
            reaction1,
        )
