from factory import DjangoModelFactory, Faker, SubFactory

from apps.users.factories import UserFactory

from .models import Post

__all__ = (
    'PostFactory'
)


class PostFactory(DjangoModelFactory):
    """Generate post with title, description and new user"""
    title = Faker('word')
    description = Faker('text')
    user = SubFactory(UserFactory)

    class Meta:
        model = Post
