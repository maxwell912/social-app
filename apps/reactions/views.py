from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from .forms import ReactionForm
from .models import Reaction

__all__ = (
    'ReactionCreate',
    'ReactionDelete',
)


class ReactionCreate(LoginRequiredMixin, CreateView):
    model = Reaction
    form_class = ReactionForm

    def get_success_url(self):
        return reverse_lazy(
            'posts:post-detail',
            args=[self.kwargs['pk']],
        )

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        user = self.request.user

        form.instance.post_id = post_id
        already_exist = not user.add_reaction(post_id, form.instance)

        if not already_exist:
            self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ReactionDelete(LoginRequiredMixin, DeleteView):
    model = Reaction

    def get_success_url(self):
        return reverse_lazy(
            'posts:post-detail',
            args=[self.kwargs['pk']],
        )

    def get_object(self, queryset=None):
        reaction = Reaction.objects.filter(
            post_id=self.kwargs['pk'],
            user_id=self.request.user.id,
            description=self.request.POST.get('description'),
        ).first()
        if not reaction:
            raise Http404
        return reaction
