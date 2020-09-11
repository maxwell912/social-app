from django.test import TestCase

from ..reactions.factories import ReactionFactory
from ..reactions.models import Reaction
from .factories import PostFactory


class TestPost(TestCase):

    def test_add_comment(self):
        """Test adding comment to post"""
        post = PostFactory()
        comment = PostFactory()
        post.add_comment(comment)
        self.assertEqual(comment.title, post.title)
        self.assertTrue(comment.is_comment)
        self.assertEqual(comment.parent_post, post)

    def test_get_reaction_count(self):
        """Test function return correct urls with count"""
        post = PostFactory()

        reactions = {
            Reaction.ANGRY: 3,
            Reaction.LIKE: 2,
        }

        for reaction, count in reactions.items():
            ReactionFactory.create_batch(
                count,
                post=post,
                description=reaction,
            )
        self.assertEqual(
            post.get_reaction_counter(),
            [
                (Reaction.IMAGE_URLS[reaction], count)
                for reaction, count in reactions.items()
            ]
        )
