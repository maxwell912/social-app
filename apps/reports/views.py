from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View

from ..posts.models import Post
from .forms import ReportForm
from .models import Report, ReportListResult
from .tasks import generate_reports
from ..posts.models import Post

__all__ = (
    'ReportListView',
    'ReportCreate',
)


class ReportListView(LoginRequiredMixin, ListView):
    template_name = 'reports/list.html'
    context_object_name = 'reports'
    queryset = Report.objects.select_related('user', 'post')
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_staff:
            return qs
        return qs.filter(user=user)


class ReportCreate(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reports/create.html'

    def get_context_data(self, **kwargs):
        """Add post_id to context"""
        context = super().get_context_data(**kwargs)
        context['post_id'] = context['view'].kwargs['pk']
        return context

    def get_success_url(self):
        return reverse_lazy(
            'posts:post-detail',
            args=[self.kwargs['pk']],
        )

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        user = self.request.user
        post = Post.objects.get(pk=post_id)

        if post.user == user:
            raise ValidationError('You cannot report your post!')

        qs = super().get_queryset()
        report = qs.filter(post_id=post_id, user_id=user.id)

        if report:
            return HttpResponseRedirect(self.get_success_url())

        report = form.instance
        report.user = user
        report.post_id = post_id
        report.save()

        return HttpResponseRedirect(self.get_success_url())


class ReportListTask(LoginRequiredMixin, View):
    """Create a ReportList task and return it's id"""
    def get(self, request, *args, **kwargs):
        task = generate_reports.delay(user_id=self.request.user.id)

        response = JsonResponse(
            {"task_id": task.task_id},
            status=202,
        )

        return response


class ReportListResultView(LoginRequiredMixin, View):
    """If task is not finished return 202, else result url"""
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs.get("task_id")

        async_result = ReportListResult.objects.filter(
            task_id=task_id,
            user=self.request.user
        ).first()

        if async_result:
            response = JsonResponse(
                {'result_url': async_result.file.url},
                status=200,
            )
            response.status_code = 200
            return response

        response = HttpResponse(request, status=202)
        return response
