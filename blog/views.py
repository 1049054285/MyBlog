from django.shortcuts import render, HttpResponse,redirect
from django.contrib import auth
import json
from blog import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from MyBlog import settings
import os, time

# Create your views here.
def func_class(request):
    from MyBlog import settings
    return {"func":settings.FUNCTION}

def index(request):
    siteCategory_list = models.SiteCategory.objects.all()

    article_list = models.Article.objects.values('nid','title','user__avatar','desc','create_time','comment_count','read_count','user__nickname','user__blog__site','read_count','comment_count','up_count','down_count')
    for article in article_list:
        article['create_time'] = article['create_time'].strftime('%Y-%m-%d %H:%M')
    #分页
    p = Paginator(article_list, 5)
    cur_page = request.GET.get('page')
    comment_list_cur = p.get_page(cur_page)
    cur_page = comment_list_cur.number
    #处理 Comment_list 为可序列化列表
    article_list = []
    for comment_obj in comment_list_cur:
        article_list.append(comment_obj)

    if request.is_ajax():
        response = {'article_list':article_list,'page':cur_page,'article_num_pages':p.num_pages}
        return HttpResponse(json.dumps(response))

    return render(request, 'index.html', locals())

def login(request):
    if request.is_ajax():
        username=request.POST.get("username")
        password=request.POST.get("password")
        verification_code=request.POST.get("verification_code")
        ajax_response={"user":None,"errors":""}
        if verification_code.upper() == request.session.get('verification_code').upper():
            user = auth.authenticate(username=username,password=password)
            if user and user.is_active:
                ajax_response['user'] = user.username
                auth.login(request, user)
            else:
                ajax_response['errors'] = '用户名或者密码错误!'
        else:
            ajax_response['errors'] = '验证码错误!'
        return HttpResponse(json.dumps(ajax_response))
    next_path = request.GET.get('next','/index/')
    return render(request, 'login.html', locals())

def reg(request):
    from . import forms
    if request.is_ajax():
        response={"flag":False,"errors":""}
        form_obj = forms.RegForm(request=request, data=request.POST)
        if form_obj.is_valid():
            username = form_obj.cleaned_data['username']
            password = form_obj.cleaned_data['password']
            email = form_obj.cleaned_data['email']
            nickname = form_obj.cleaned_data['nickname']
            avatar_file = request.FILES.get('img_avatar')
            user_obj = models.UserInfo.objects.create_user(username=username,password=password,email=email,nickname=nickname,avatar=avatar_file)
            #默认新建Blog用户主站
            blog_obj = models.Blog.objects.create(title='%s的博客'%nickname,site=username,theme='%s.css'%username)
            #关联用户和博客主站
            user_obj.blog = blog_obj
            user_obj.save()
            ##新建 default 个人站点文章分类
            models.HomeCategory.objects.create(title='默认分类',blog=blog_obj)
            response['flag'] = True
        else:
            response['errors'] = form_obj.errors
        return HttpResponse(json.dumps(response))

    reg_form = forms.RegForm(request=request)
    return render(request, 'reg.html', locals())

def get_verification_code(request):
    import random
    from io import BytesIO
    from PIL import Image, ImageDraw, ImageFont
    f = BytesIO()
    img = Image.new(mode='RGB', size=(120,30), color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    draw = ImageDraw.Draw(img, mode='RGB')
    font=ImageFont.truetype("blog/static/bs/fonts/kumo.ttf", size=28)
    code_list = []
    for i in range(1,6):
        code_text = random.choice([chr(random.randint(65,90)), chr(random.randint(97,122)), str(random.randint(0,9))])
        code_list.append(code_text)
        draw.text((i*20,0), code_text, font=font)
    img.save(f, 'png')

    verification_code_text = ''.join(code_list)
    request.session["verification_code"] = verification_code_text
    return HttpResponse(f.getvalue())

def logout(request):
    auth.logout(request)
    return redirect('/login/')

#########################Home
import datetime
from django.db.models import Count
from django.db.models import F, Q
from django.db.utils import IntegrityError

def home_site(request, user_site, **kwargs):
    user = models.UserInfo.objects.filter(blog__site=user_site).first()
    if not user:
        return render(request, 'not_found.html')
    else:
        tags_list = models.Article.objects.filter(user=user).values_list('tags__title','tags__nid').exclude(tags__title=None).annotate(count=Count('nid')).order_by('count').reverse()
        homeCategory_list = models.Article.objects.filter(user=user).values_list('homeCategory__title','homeCategory__nid').annotate(count=Count('nid')).order_by('count').reverse()
        cur_date = datetime.datetime.now().replace(year=2030)
        top_three_article_list = models.Article.objects.filter(user=user).order_by('read_count').reverse()[:4]
        archive_list = models.Article.objects.archive(user=user)
        if kwargs:
            if kwargs['condition'] == 'tag':
                article_list = models.Article.objects.filter(user=user,tags__nid=kwargs['para']).all()
            elif kwargs['condition'] == 'homecategory':
                article_list = models.Article.objects.filter(user=user,homeCategory__nid=kwargs['para']).all()
            elif kwargs['condition'] == 'date':
                article_list = models.Article.objects.filter(user=user,create_time__contains=kwargs['para']).all()
            else:
                article_list = models.Article.objects.filter(user=user).all()
                return render(request, 'home_site.html', locals())
        else:
            article_list = models.Article.objects.filter(user=user).all()
        return render(request, 'home_site.html', locals())

def article_detail(request, user_site, article_id):
    ################################ 处理多级评论
    from collections import OrderedDict
    comment_dict = OrderedDict()
    comment_list = models.Comment.objects.filter(article_id=article_id).order_by('create_time').values('create_time','user__blog__site','user__nickname','user_id','up_count','parent_comment_id','nid','content','article_id')
    for comment_obj in comment_list:
        comment_obj['children_comment'] = []
        comment_dict[comment_obj['nid']] = comment_obj
    for nid in comment_dict:
        comment_dict[nid]['create_time'] = comment_dict[nid]['create_time'].strftime('%Y-%m-%d %H:%M:%S')
    comment_list = [] #储存最终Comment_list 结果
    for nid in comment_dict:
        if comment_dict[nid]['parent_comment_id']:
            pid = comment_dict[nid]['parent_comment_id']
            comment_dict[pid]['children_comment'].append(comment_dict[nid])
        else:
            comment_list.append(comment_dict[nid])
    #处理多级评论 后 分页
    p = Paginator(comment_list, 5)
    cur_page = request.GET.get('page')
    comment_list_cur = p.get_page(cur_page)
    cur_page = comment_list_cur.number
    #处理 Comment_list 为可序列化列表
    comment_list = list(comment_list_cur)
    # 添加评论楼层数
    new_comment_list = []
    for i,comment_obj in enumerate(comment_list_cur,1):
        comment_obj['floor_num'] = i+(cur_page-1)*5
        new_comment_list.append(comment_obj)
    ###################################### 到此评论数据处理完毕

    ###################################  AJAX加载评论内容时，评论数据发送给客户端
    if request.is_ajax():
        #添加当前页面到发送的数据里
        response = {}
        response['comment_list'] = new_comment_list
        response['page'] = cur_page
        response['comment_num_pages'] = p.num_pages
        # print(' get ajax request page: ', cur_page)
        return HttpResponse(json.dumps(response))


    ########################################以下是GET请求才会加载
    #文章作者
    user = models.UserInfo.objects.filter(blog__site=user_site).first()
    #本文章
    article = models.Article.objects.filter(nid=article_id).first()
    #标签
    tags_list = models.Article.objects.filter(user=user).values_list('tags__title','tags__nid').exclude(tags__title=None).annotate(count=Count('nid')).order_by('count').reverse()
    #分类
    homeCategory_list = models.Article.objects.filter(user=user).values_list('homeCategory__title','homeCategory__nid').annotate(count=Count('nid')).order_by('count').reverse()
    #归档日期
    cur_date = datetime.datetime.now().replace(year=2030)
    archive_list = models.Article.objects.archive(user=user)
    #阅读排行榜
    top_three_article_list = models.Article.objects.filter(user=user).order_by('read_count').reverse()[:4]
    #统计文章阅读数
    models.Article.objects.filter(nid=article_id).update(read_count=F('read_count')+1)
    return render(request, 'article_detail.html', locals())

def article_up_down(request):
    response = {'result':'fail','up_count':0}
    article_id = request.POST.get('article_id')
    user = request.user
    is_up = bool(request.POST.get('is_up'))
    a_updown_obj = None
    try:
        a_updown_obj = models.ArticleUpDown.objects.create(article_id=article_id, user=user, is_up=is_up)
    except IntegrityError:
        response['result'] = 'is_exist'
    if a_updown_obj:
        rows = models.Article.objects.filter(nid=article_id).update(up_count=F('up_count')+1)
        if rows == 1:
            response['result'] = 'success'
        response['up_count'] = models.Article.objects.filter(nid=article_id).values_list('up_count')[0][0]
    return HttpResponse(json.dumps(response))

def comment(request):
    response = {'result':'fail','comment_count':0,'comment_id':'','create_time':''}
    article_id = request.POST.get('article_id')
    comment_cont = request.POST.get('comment_cont')
    if comment_cont.endswith('\n'):
        comment_cont = comment_cont[:-1]
    parent_comment_id = request.POST.get('parent_comment_id')
    edit_comment_id = request.POST.get('edit_comment_id')
    user = request.user
    comment_obj, rows = None, None
    if parent_comment_id:
        comment_obj = models.Comment.objects.create(article_id=article_id, content=comment_cont, user=user, parent_comment_id=parent_comment_id)
    elif edit_comment_id:
        rows = models.Comment.objects.filter(nid=edit_comment_id).update(content=comment_cont)
    else:
        comment_obj = models.Comment.objects.create(article_id=article_id, content=comment_cont, user=user)
    if comment_obj:
        rows = models.Article.objects.filter(nid=article_id).update(comment_count=F('comment_count')+1)
        if rows == 1:
            response['result'] = 'success'

    if rows == 1:
        response['result'] = 'success'
    response['comment_count'] = models.Article.objects.filter(nid=article_id).values_list('comment_count')[0][0]

    return HttpResponse(json.dumps(response))

def comment_up(request):
    response = {'result':'fail','up_count':''}
    comment_id = request.POST.get('comment_id')
    user = request.user
    comment_up_obj = None
    try:
        comment_up_obj = models.CommentUp.objects.create(user=user,comment_id=comment_id)
    except IntegrityError:
        response['result'] = 'is_exist'
    if comment_up_obj:
        rows = models.Comment.objects.filter(nid=comment_id).update(up_count=F('up_count')+1)
        if rows == 1:
            response['result'] = 'success'
        response['up_count'] = models.Comment.objects.filter(nid=comment_id).values_list('up_count')[0][0]
    return HttpResponse(json.dumps(response))

def del_comment(request):
    response = {'result':'fail','comment_count':0}
    comment_id = request.POST.get('comment_id')
    article_id = request.POST.get('article_id')
    user = request.user
    rows ,dic= models.Comment.objects.filter(nid=comment_id,user=user).delete()
    if rows >= 1:
        rows = models.Comment.objects.filter(article_id=article_id).count()
        rows = models.Article.objects.filter(nid=article_id).update(comment_count=rows)
        if rows == 1:
            response['result'] = 'success'
        response['comment_count'] = models.Article.objects.filter(nid=article_id).values_list('comment_count')[0][0]
    return HttpResponse(json.dumps(response))

##################backstage
def backstage(request,username):
    article_list = models.Article.objects.filter(user=request.user).values('nid','title','create_time','comment_count','read_count','user__blog__site')
    for article in article_list:
        article['create_time'] = article['create_time'].strftime('%Y-%m-%d %H:%M')
    #分页
    p = Paginator(article_list, 5)
    cur_page = request.GET.get('page')
    comment_list_cur = p.get_page(cur_page)
    cur_page = comment_list_cur.number
    #处理 Comment_list 为可序列化列表
    article_list = []
    for comment_obj in comment_list_cur:
        article_list.append(comment_obj)

    if request.is_ajax():
        response = {'article_list':article_list,'page':cur_page,'article_num_pages':p.num_pages}
        return HttpResponse(json.dumps(response))

    return render(request, 'backstage.html', locals())

def add_article(request):
    if request.method == 'POST':
        print('in method add_aarticle')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        homeCategory_id = request.POST.get('homeCategory')
        tag_id_list = request.POST.getlist('tag')
        siteSubCategory_id = request.POST.get('siteSubCategory')
        article_content = request.POST.get('article_content')
        a_obj = models.Article.objects.create(title=title,desc=desc,user=request.user,homeCategory_id=homeCategory_id,siteSubCategory_id=siteSubCategory_id)
        models.ArticleDetail.objects.create(content=article_content,article=a_obj)
        for tag_id in tag_id_list:
            models.Article2Tag.objects.create(article=a_obj,tag_id=tag_id)
        return redirect(to='/backstage/%s'%request.user.username)

    homeCategory_list = models.HomeCategory.objects.filter(blog__userinfo=request.user).all()
    siteSubCategory_list = models.SiteSubCategory.objects.all()
    tag_list = models.Tag.objects.filter(blog__userinfo=request.user).all()

    return render(request, 'add_article.html', locals())

def del_article(request):
    article_id = request.GET.get('article_id')
    models.Article.objects.filter(nid=article_id).delete()
    return HttpResponse('ok')

def edit_article(request):
    if request.method == 'POST':
        formData = dict(request.POST)
        models.Article.objects.filter(nid=formData['id'][0]).update(title=formData['title'][0],desc=formData['desc'][0],homeCategory_id=formData['homeCategory'][0],siteSubCategory_id=formData['siteSubCategory'][0])
        models.Article2Tag.objects.filter(article_id=formData['id'][0]).delete()
        for tag_id in formData['tag']:
            models.Article2Tag.objects.create(article_id=formData['id'][0],tag_id=tag_id)
        rows = models.ArticleDetail.objects.filter(article_id=formData['id'][0]).update(content=formData['content'][0])
        return HttpResponse('ok')
    article_id = request.GET.get('article_id')
    article_values = models.Article.objects.filter(nid=article_id).values('title','desc','homeCategory_id','siteSubCategory_id','articledetail__content').first()
    article_values = dict(article_values)
    tags_values = models.Article.objects.filter(nid=article_id).values('tags__nid').all()
    article_tag_ids = []
    for item in tags_values:
        article_tag_ids.append(item['tags__nid'])
    article_values['tags_id'] = article_tag_ids
    homeCategory_values = models.HomeCategory.objects.filter(blog__userinfo=request.user).values('nid','title')
    homeCategory_list = []
    for homeCategory in homeCategory_values:
        homeCategory_list.append(homeCategory)
    siteSubCategory_values = models.SiteSubCategory.objects.values('nid','name')
    siteSubCategory_list = []
    for siteSubCategory in siteSubCategory_values:
        siteSubCategory_list.append(siteSubCategory)
    tag_values = models.Tag.objects.filter(blog__userinfo=request.user).values('nid','title')
    tag_list = []
    for tag in tag_values:
        tag_list.append(tag)
    response = {'homeCategory_list':homeCategory_list,'siteSubCategory_list':siteSubCategory_list,'tag_list':tag_list,'article_values':article_values}
    return HttpResponse(json.dumps(response))










