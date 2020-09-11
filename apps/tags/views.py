from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from ..posts.models import Post
from .forms import TagForm
from .models import Tag

__all__ = (
    'TagCreate',
)


class TagCreate(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'tags/create.html'

    def get_context_data(self, **kwargs):
        """Add post comments to context"""
        post_id = self.kwargs['pk']

        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=post_id)
        return context

    def get_success_url(self):
        return reverse_lazy(
            'posts:post-update',
            args=[self.kwargs['pk']],
        )

    def form_valid(self, form):
        """If tag already exist add it to post

        Else create new one and add
        """
        self.create_or_add_tag(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        """If there is only unique error return form_valid"""
        title_errors = form.errors['title']
        if title_errors and title_errors.data:
            error_data = title_errors.data
            if len(error_data) == 1 and error_data[0].code == 'unique':
                self.create_or_add_tag(form)
                return HttpResponseRedirect(self.get_success_url())
        return super().form_invalid(form)

    def create_or_add_tag(self, form):
        title = form.instance.title
        tag = Tag.objects.filter(title=title).first()
        if tag:
            self.add_tag_to_post(tag, self.kwargs['pk'])
            return HttpResponseRedirect(self.get_success_url())

        tag = form.instance
        tag.save()
        self.add_tag_to_post(tag, self.kwargs['pk'])

    def add_tag_to_post(self, tag: Tag, post_id: int):
        """Add tag to post with certain id"""
        post = Post.objects.get(pk=post_id)
        tag.posts.add(post)


class TagDelete(LoginRequiredMixin, DeleteView):
    model = Tag

    def get_success_url(self):
        return reverse_lazy(
            'posts:post-update',
            args=[self.kwargs['pk']],
        )

    def get_object(self, queryset=None):
        tag = Tag.objects.filter(
            title=self.request.POST.get('title')
        ).first()
        if not tag:
            raise Http404
        return tag

    def delete(self, request, *args, **kwargs):
        """If user has permission and tag exists remove it from post"""

        tag = self.get_object()
        success_url = self.get_success_url()

        post = Post.objects.get(pk=self.kwargs['pk'])
        if tag and request.user.id == post.user_id:
            tag.posts.remove(post)

        return HttpResponseRedirect(success_url)
