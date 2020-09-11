from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views import View
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Post, AttachmentsResult
from .forms import PostForm, CommentForm, PostCreateForm
from ..reactions.forms import ReactionForm
from ..tags.forms import TagForm
from ..files.models import File
from .tasks.save_attachments import generate_zip

__all__ = (
    'PostListView',
    'PostCreate',
    'PostDetailView',
    'CommentCreate',
    'PostUpdate',
    'AttachmentsZipView',
    'create_task',
    'PostDeleteView',
)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'
    paginate_by = 5

    extra_context = {
        'comment_form': CommentForm,
        'reaction_form': ReactionForm,
    }

    def get_context_data(self, **kwargs):
        """Add post comments to context"""
        context = super().get_context_data(**kwargs)
        post = context['post']
        page_num = self.request.GET.get('page', 1)

        can_report = False
        if self.request.user.is_authenticated:
            user = self.request.user
            already_reported = user.reports.filter(post_id=post.id).first()
            post_owner = post.user_id == user.id
            can_report = not (post_owner or already_reported)

        comment_page = Paginator(
            post.active_comments(),
            self.paginate_by
        ).get_page(page_num)

        context['comment_page'] = comment_page
        context['can_report'] = can_report
        context['is_author'] = self.request.user.id == post.user_id
        return context


class PostListView(ListView):
    queryset = (
        Post.objects.feed()
            .prefetch_related('tags')
            .select_related('user')
    )

    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 10

    attr_name2db_check = {
        'Author': 'user__email__icontains',
        'Title': 'title__icontains',
        'Text': 'description__icontains',
        'Tag': 'tags__title__icontains',
    }

    extra_context = {'filter_attrs': attr_name2db_check.keys()}

    def get_queryset(self):
        """Return posts filtered by attributes value

        If request has 'attr' attribute return queryset of objects
        whose certain attribute contains 'substring' attribute
        """
        posts = super().get_queryset() \
            .annotate(
                in_favorite=Count(
                    'bookmarks',
                    filter=Q(bookmarks__user_id=self.request.user.id)
                )
            )
        data = self.kwargs
        filter_attr = data.get('attr')
        if not filter_attr:
            return posts
        substring = data.get('substring')
        params = {
            self.attr_name2db_check[filter_attr]:
                substring
        }
        return posts.filter(**params)


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('posts:post-list')

    def form_valid(self, form):
        """Set current user and attach files and tags to the created Post"""
        form.instance.user = self.request.user
        self.object = form.save()

        for tag in form.cleaned_data['tags']:
            self.object.add_tag(title=tag)

        files = self.request.FILES.getlist('attachments')
        for file in files:
            File(
                file=file,
                post=self.object,
            ).save()

        return HttpResponseRedirect(self.get_success_url())


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/update.html'

    context_object_name = 'post'
    extra_context = {'tag_form': TagForm}

    def get_success_url(self):
        return reverse_lazy(
            'posts:post-detail',
            args=[self.kwargs['pk']],
        )

    def form_valid(self, form):
        """Update post attachments"""
        files = self.request.FILES.getlist('attachments')
        for file in files:
            File(
                file=file,
                post=self.object,
            ).save()

        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('posts:post-list')
    queryset = Post.objects.select_related('user')

    def get_object(self, queryset=None):
        """Check that user wants to delete his post.

        Return post or error.
        """
        post = super().get_object()
        if post.user_id == self.request.user.id:
            return post
        else:
            raise ValidationError("You cannot delete this post!")


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CommentForm
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy(
            'posts:post-detail',
            args=[self.kwargs['pk']],
        )

    def form_valid(self, form):
        comment = form.instance
        comment.user = self.request.user

        parent_post_id = self.kwargs['pk']
        parent_post = Post.objects.get(pk=parent_post_id)
        parent_post.add_comment(comment)
        return super().form_valid(form)


def create_task(request, pk):
    """Create a task and return task id."""
    task = generate_zip.delay(post_id=pk)

    response = JsonResponse({"task_id": task.task_id})
    response.status_code = 202

    return response


class AttachmentsZipView(View):
    """Class for creating task that saves all attached post files to zip."""

    def get(self, request, *args, **kwargs):
        """Return response 202 if task is not finished, else result zip url."""
        task_id = self.kwargs.get("task_id")
        attachments_zip = AttachmentsResult.objects.filter(
            task_id=task_id,
        ).first()

        if attachments_zip:
            response = JsonResponse({'result_url': attachments_zip.zip_file.url})
            response.status_code = 200
            return response

        response = HttpResponse(request)
        response.status_code = 202
        return response
