from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

from ..posts.models import Post


class BookmarkCreate(View):
    model = None
    success_url = reverse_lazy('posts:post-list')

    def post(self, request, pk):
        """Add or remove post to favorites."""
        user = request.user
        post = Post.objects.get(id=pk)

        if post.is_comment:
            return render(
                request,
                'bookmarks/comment.html',
                {'message': 'You cannot add a comment to favorites!'}
            )

        self.model.objects.get_or_create(
            user=user,
            post_id=pk
        )
        return HttpResponseRedirect(self.success_url)


class BookmarkDelete(DeleteView):
    model = None
    success_url = reverse_lazy('posts:post-list')

    def get_object(self, queryset=None):
        post_id = self.kwargs['pk']
        user = self.request.user

        return self.model.objects.get(
            post_id=post_id,
            user_id=user.id,
        )


class UserBookmarkedPostsView(ListView):
    """Render page with favorite posts."""
    queryset = (
        Post.objects.feed()
            .select_related('user')
            .prefetch_related('tags', 'bookmarks')
    )

    context_object_name = 'bookmarks'
    template_name = 'bookmarks/list.html'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            bookmarks__user_id=self.kwargs['pk'],
        )
