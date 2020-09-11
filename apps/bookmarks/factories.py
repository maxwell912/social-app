import factory
from factory import SubFactory

from ..posts.factories import PostFactory
from ..users.factories import UserFactory
from .models import BookmarkPost

__all__ = (
    'BookmarkFactory'
)


class BookmarkFactory(factory.DjangoModelFactory):
    user = SubFactory(UserFactory)
    post = SubFactory(PostFactory)

    class Meta:
        model = BookmarkPost
