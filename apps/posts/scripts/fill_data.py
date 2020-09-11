from apps.posts.factories import PostFactory
from apps.reports.factories import ReportFactory
from apps.users.factories import UserFactory


def run(**kwargs):
    """Generate 'number' of users with 5 posts

    with 3 comments on each created by different users
    """
    number = kwargs.get('number', 5)

    if number < 1:
        raise ValueError("Incorrect 'number' argument")

    for user in UserFactory.create_batch(number):
        for num, post in enumerate(PostFactory.create_batch(5, user=user)):
            for comment in PostFactory.create_batch(3):
                post.add_comment(comment)

            if num % 3 == 0:
                ReportFactory(
                    post=post,
                )
