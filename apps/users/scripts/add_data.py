from random import choice, sample

from ...bookmarks.factories import BookmarkFactory
from ...posts.factories import PostFactory
from ...posts.models import Post
from ...reactions.factories import ReactionFactory
from ...reports.factories import ReportFactory
from ...tags.factories import TagFactory
from ..factories import UserFactory
from ..models import User

USERS_COUNT = 70
POSTS_PER_USER = 15
COMMENTS_COUNT = 5


def run(**kwargs):
    users = list(UserFactory.create_batch(USERS_COUNT))

    for user in users:
        for _ in range(POSTS_PER_USER):
            post = PostFactory(user=user)
            ReactionFactory.create(post=post)
            TagFactory(posts=post)

    posts = list(Post.objects.all())

    for user in sample(users, 10):
        for post in sample(posts, 10):

            if post.user != user:
                ReportFactory(post=post, user=user)

            for comment in PostFactory.create_batch(COMMENTS_COUNT, user=user):
                post.add_comment(comment)

    user = choice(users)
    for post in sample(posts, 10):
        BookmarkFactory(user=user, post=post)
