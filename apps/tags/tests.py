from unittest.mock import MagicMock

from django.test import TestCase

from apps.posts.factories import PostFactory

from .factories import TagFactory
from .models import Tag
from .views import TagCreate


class TagTestCase(TestCase):

    def setUp(self):
        """Create new post, user and ReactionView."""
        self.post = PostFactory()

        self.view = TagCreate()
        self.view.kwargs = {'pk': self.post.id}

        self.request = MagicMock()

        self.view.request = self.request

    def test_tag_description(self):
        """Check exists tag's title."""
        tag = TagFactory()
        self.assertTrue(hasattr(tag, 'title'))

    def test_adding_tag(self):
        """Test POST request with new tag creates tag"""
        self.assertIsNone(Tag.objects.filter(title='new_tag').first())

        self.request.method = 'POST'
        self.request.POST = {'title': 'new_tag'}
        self.view.post(self.request, pk=self.post.id)

        self.assertIsNotNone(Tag.objects.filter(title='new_tag').first())

    def test_adding_similar_tag(self):
        """Test adding similar tags creates only 1"""
        post = PostFactory()

        self.request.method = 'POST'
        self.request.POST = {'title': 'new_tag'}
        self.view.post(self.request, pk=self.post.id)
        self.view.post(self.request, pk=post.id)

        self.assertEqual(Tag.objects.filter(title='new_tag').count(), 1)
