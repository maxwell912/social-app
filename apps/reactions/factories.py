import factory
from factory import SubFactory, fuzzy

from ..posts.factories import PostFactory
from ..users.factories import UserFactory
from .models import Reaction

__all__ = (
    'ReactionFactory'
)


class ReactionFactory(factory.DjangoModelFactory):
    """Generate reaction with description."""
    description = fuzzy.FuzzyChoice([Reaction.SAD, Reaction.LIKE])
    user = SubFactory(UserFactory)
    post = SubFactory(PostFactory)

    class Meta:
        model = Reaction
