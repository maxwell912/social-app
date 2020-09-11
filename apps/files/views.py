from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView

from apps.files.models import File


class FileDetail(DetailView):
    model = File
    template_name = 'files/detail.html'
    context_object_name = 'file'


class FileDelete(LoginRequiredMixin, DeleteView):
    model = File

    def post(self, request, *args, **kwargs):
        """If user has permission and operation wasn't canceled delete file"""
        user = request.user
        file = self.get_object()

        self.success_url = reverse_lazy(
            'posts:post-update',
            args=[file.post_id],
        )

        if user.id != file.post.user_id:
            return HttpResponseRedirect(self.success_url)
        return super().post(request, *args, **kwargs)
