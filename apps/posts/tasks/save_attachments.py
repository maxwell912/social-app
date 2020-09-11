from __future__ import absolute_import, unicode_literals

import os
import pathlib

from zipfile import ZipFile
from celery import shared_task
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile

from ..models import AttachmentsResult, Post


def save_attachments(post, path, filename):
    """Create zip file of all attachments of post."""
    if not os.path.exists(path):
        os.makedirs(path)

    my_file = SimpleUploadedFile(path / filename, '')
    uploaded = UploadedFile(file=my_file)
    with ZipFile(uploaded.file, 'w') as z:
        for file in post.attachments.all():
            filename = pathlib.PurePosixPath(file.file.path).name
            z.write(file.file.path, filename)

    return uploaded


@shared_task(bind=True)
def generate_zip(self, post_id: int):
    """Store for download, and save the download URL when task finishes."""
    post = Post.objects.filter(id=post_id).first()
    filename = f"post_{post.id}.zip"

    path = AttachmentsResult.PATH / str(post_id)

    file = save_attachments(post, path, filename)
    task_id = self.request.id

    AttachmentsResult.objects.create(
        task_id=task_id,
        zip_file=file,
        post_id=post_id,
    )
