# Generated by Django 3.0.8 on 2020-08-25 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentsResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255, verbose_name='Task id')),
                ('zip_file', models.FileField(upload_to='media/attachments', verbose_name='Zip file')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
            ],
            options={
                'verbose_name': 'Attachments',
                'verbose_name_plural': 'Attachments',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=255, verbose_name='Description')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')),
                ('deleted_at', models.DateTimeField(null=True, verbose_name='Date of deleting')),
                ('comment_allowed', models.BooleanField(default=True, verbose_name='Post can be commented')),
                ('is_comment', models.BooleanField(default=False, verbose_name='Post is a comment')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('parent_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.Post')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ('-created_at',),
            },
        ),
    ]
