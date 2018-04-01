from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class ArticleManager(models.Manager):
    """文章按照日期归档"""

    def archive(self, **kwargs):
        archive_list = []
        articles_time = self.filter(**kwargs).order_by('create_time').values_list('create_time')
        tmp_time_list = []
        for i in articles_time:
            time = i[0].strftime('%Y-%m-%d %H')
            if time not in tmp_time_list:
                count = Article.objects.filter(create_time__icontains=time).count()
                archive_list.append((time, count))
                tmp_time_list.append(time)
        return archive_list


class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    telephone = models.CharField(verbose_name='手机号码', max_length=11, null=True, unique=True)
    avatar = models.FileField(verbose_name='头像', upload_to='avatar/', default="/avatar/default.jpg")
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)
    blog = models.OneToOneField(verbose_name='个人博客', to='Blog', to_field='nid', null=True, on_delete=models.CASCADE)
    fans = models.ManyToManyField(verbose_name='粉丝们', to='UserInfo', through='UserFans',
                                  through_fields=('user', 'follower'))

    def __str__(self):
        return self.username


class UserFans(models.Model):
    """互粉关系表，用户表多对多用户表"""
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users',
                             on_delete=models.CASCADE)
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers',
                                 on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]


class Blog(models.Model):
    """
    博客信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)

    def __str__(self):
        return self.title


class HomeCategory(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    read_count = models.IntegerField(verbose_name='阅读数', default=0)
    comment_count = models.IntegerField(verbose_name='评论数', default=0)
    up_count = models.IntegerField(verbose_name='点赞数', default=0)
    down_count = models.IntegerField(verbose_name='踩灭数', default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    homeCategory = models.ForeignKey(verbose_name='博主个人文章类型', to='HomeCategory', to_field='nid', null=True,
                                     on_delete=models.CASCADE)
    siteSubCategory = models.ForeignKey(verbose_name='网站子类型', to='SiteSubCategory', to_field='nid', null=True,
                                        on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='nid', on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )
    objects = ArticleManager()

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid', on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容', )
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid', on_delete=models.CASCADE)


class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    up_count = models.IntegerField(verbose_name='点赞数', default=0)
    parent_comment = models.ForeignKey(verbose_name='父级评论', to='self', null=True, default=None, on_delete=models.CASCADE)


class ArticleUpDown(models.Model):
    """
    文章点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='点赞者', to='UserInfo', to_field='nid', null=False, on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid', null=False, on_delete=models.CASCADE)
    is_up = models.BooleanField(verbose_name='是否赞', default=True)

    class Meta:
        unique_together = [
            ('article', 'user', 'is_up'),
        ]

    def __str__(self):
        return str(self.is_up)


class CommentUp(models.Model):
    """
    评论点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='点赞者', to='UserInfo', to_field='nid', null=False, on_delete=models.CASCADE)
    comment = models.ForeignKey(verbose_name='评论', to="Comment", to_field='nid', null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('comment', 'user'),
        ]


class SiteCategory(models.Model):
    """网站分类表"""
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='网站分类名', max_length=32, unique=True)

    def __str__(self):
        return self.name


class SiteSubCategory(models.Model):
    """网站子分类表"""
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='网站子分类名', max_length=32, unique=True)
    siteCategory = models.ForeignKey("SiteCategory", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
