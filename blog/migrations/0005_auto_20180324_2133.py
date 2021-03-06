# Generated by Django 2.0.3 on 2018-03-24 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_article_sitesubcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentUp',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserFans',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='read_count',
            field=models.IntegerField(default=0, verbose_name='阅读数'),
        ),
        migrations.AddField(
            model_name='comment',
            name='up_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='comment_count',
            field=models.IntegerField(default=0, verbose_name='评论数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='down_count',
            field=models.IntegerField(default=0, verbose_name='踩灭数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='homeCategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.HomeCategory', verbose_name='博主个人文章类型'),
        ),
        migrations.AlterField(
            model_name='article',
            name='siteSubCategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.SiteSubCategory', verbose_name='网站子类型'),
        ),
        migrations.AlterField(
            model_name='article',
            name='up_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AlterField(
            model_name='articledetail',
            name='article',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='所属文章'),
        ),
        migrations.AlterField(
            model_name='articledetail',
            name='content',
            field=models.TextField(verbose_name='文章内容'),
        ),
        migrations.AlterField(
            model_name='articleupdown',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='文章'),
        ),
        migrations.AlterField(
            model_name='articleupdown',
            name='is_up',
            field=models.BooleanField(default=True, verbose_name='是否赞'),
        ),
        migrations.AlterField(
            model_name='articleupdown',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞者'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Comment', verbose_name='父级评论'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='/avatar/default.jpg', upload_to='avatar/', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='blog',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog', verbose_name='个人博客'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='telephone',
            field=models.CharField(max_length=11, null=True, unique=True, verbose_name='手机号码'),
        ),
        migrations.AddField(
            model_name='userfans',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='粉丝'),
        ),
        migrations.AddField(
            model_name='userfans',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='博主'),
        ),
        migrations.AddField(
            model_name='commentup',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Comment', verbose_name='评论'),
        ),
        migrations.AddField(
            model_name='commentup',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞者'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='fans',
            field=models.ManyToManyField(through='blog.UserFans', to=settings.AUTH_USER_MODEL, verbose_name='粉丝们'),
        ),
        migrations.AlterUniqueTogether(
            name='userfans',
            unique_together={('user', 'follower')},
        ),
        migrations.AlterUniqueTogether(
            name='commentup',
            unique_together={('comment', 'user')},
        ),
    ]
