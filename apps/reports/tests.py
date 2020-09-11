from unittest.mock import MagicMock, patch

from django.test import TestCase

from apps.posts.factories import PostFactory
from apps.reports.factories import ReportFactory
from apps.reports.models import Report
from apps.reports.views import ReportCreate
from apps.users.factories import UserFactory


class TestReports(TestCase):

    @patch('apps.reports.signals.disable_post')
    def test_post_disable(self, mock):
        """Reports from 3 different user block post"""
        post = PostFactory(is_active=True)
        ReportFactory.create_batch(3, post=post)
        self.assertFalse(post.is_active)

    def test_report_only_once(self):
        """Report can be sent only once"""
        user = UserFactory()
        post = PostFactory()

        request = MagicMock()
        request.user = user
        request.method = 'POST'
        request.POST = {'reason': Report.HARASSMENT}

        view = ReportCreate()
        view.kwargs = {'pk': post.id}
        view.request = request

        view.post(request, pk=post.id)
        view.post(request, pk=post.id)

        self.assertEqual(post.reports.count(), 1)
        self.assertEqual(user.reports.count(), 1)
