import factory

from .models import User

__all__ = (
    'UserFactory'
)


class UserFactory(factory.DjangoModelFactory):
    """Generate user with title, description and new user"""
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = User
        django_get_or_create = ('email',)
