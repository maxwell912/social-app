from factory import DjangoModelFactory, SubFactory, fuzzy

from ..posts.factories import PostFactory
from ..users.factories import UserFactory
from .models import Report

__all__ = (
    'ReportFactory'
)


class ReportFactory(DjangoModelFactory):
    reason = fuzzy.FuzzyChoice([Report.EXTREMISM, Report.HARASSMENT])
    user = SubFactory(UserFactory)
    post = SubFactory(PostFactory)

    class Meta:
        model = Report
