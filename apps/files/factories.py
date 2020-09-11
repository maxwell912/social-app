import factory

from .models import File

__all__ = (
    'FileFactory'
)


class FileFactory(factory.DjangoModelFactory):
    """Generate file with path."""
    path = factory.Faker('name')

    class Meta:
        model = File
        django_get_or_create = ('path',)
