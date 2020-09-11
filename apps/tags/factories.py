import factory
from factory import fuzzy, post_generation

from .models import Tag

__all__ = (
    'TagFactory'
)


class TagFactory(factory.DjangoModelFactory):
    """Generate tag with title."""
    title = fuzzy.FuzzyText(length=10).FACTORY_BUILDER_PHASE

    class Meta:
        model = Tag
        django_get_or_create = ('title',)

    @post_generation
    def posts(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.posts.add(extracted)
            extracted.tags.add(self)
