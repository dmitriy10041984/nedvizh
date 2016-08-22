from django.http.response import HttpResponse, Http404, HttpResponseRedirect
#отвечает за получение шаблона
from django.template.loader import get_template
#отвечает за хранение переменных, которые будут огтправлены потом в шаблон
from django.template import loader, Context, RequestContext
from django.shortcuts import render_to_response, redirect, render
from article.models import Article, Comments, Category, Keywords, Author, Home, Cloudtegs
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.core.paginator import Paginator
from django.contrib import auth
from article.forms import CommentForm, KeywordsForm
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
import operator

#не рабочая
#from secondapp.forms import CommentForm
#---------------------------------------------------


# Create your views here.

def basic_one(request):
    view = "basic_one"
    html = "<html><body>This is %s view</html></body>" % view
    return HttpResponse(html)


def template_two(request):
    view = "template_two"
    t = get_template('myview.html')
    html = t.render(Context({'name': view}))
    return HttpResponse(html)


def template_three_simple(request):
    view = "template_three"
    return render_to_response('myview.html', {'name': view})




def articles(request, page_number=1):
    # связь с формой
    keywords_form = KeywordsForm
    args = {}
    all_articles = Article.objects.all()
    current_page = Paginator(all_articles, 100)
    args['articles'] = current_page.page(page_number)
    args['keywords'] = Keywords.objects.all()
    args['cloudtegs'] = Cloudtegs.objects.all()
    args['projects'] = Category.objects.all()
    args['username'] = auth.get_user(request).username
    args['authors'] = Author.objects.all()
    args['form_keywords'] = keywords_form
    return render_to_response('articles.html', args)


def article(request, article_id=1):
    # связь с формой
    keywords_form = KeywordsForm
    comment_form = CommentForm
    args = {}
    args.update(csrf(request))
    args['projects'] = Category.objects.all()
    args['article'] = Article.objects.get(id=article_id)
    args['category'] = Category.objects.filter(id=article_id)
    args['comments'] = Comments.objects.filter(comments_article_id=article_id)
    args['n_comments'] = args['comments'].count()
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    args['keywords'] = Keywords.objects.all()
    args['cloudtegs'] = Cloudtegs.objects.all()
    args['authors'] = Author.objects.all()
    args['form_keywords'] = keywords_form

    return render_to_response('article.html', args)


def addcomment(request, article_id):

    if request.POST and ("pause" not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_article = Article.objects.get(id=article_id)
            #получение автора с запроса
            comment.comments_author = request.user
            form.save()
            request.session.set_expiry(60)
            request.session['pause'] = True
    return redirect('/articles/get/%s/' % article_id)


#Выберем все статьи, которые имеют выбранный тег поиска
@csrf_exempt
def keywords(request):
    #связь с формой. Инстанс класса - получение экземпляра класса внутри функции
    keywords_form = KeywordsForm(request.POST)
    #путь для возвращения на предыдущую страницу, если запрос не POST
    return_path = request.META.get('HTTP_REFERER', '/')
    args = {}
    args['keywords'] = Keywords.objects.all()
    args['cloudtegs'] = Cloudtegs.objects.all()
    #конкретный тег по нашему id
    #для поискка не нужна args['keyw_s'] = Keywords.objects.get(id=id)
    #статьи, фильтр который по статьям имеет точное совпадение. Данная строка фильтра связывает 2 поля: keywords и name
    #args['articles'] = Article.objects.filter(keywords__name__exact=args['keyw_s'])
    #Данная переменная нужна для того чтобы на данной странице отобразить дерево категорий
    args['projects'] = Category.objects.all()
    args['username'] = auth.get_user(request).username
    args['authors'] = Author.objects.all()
    #для вывода формы
    args['form_keywords'] = keywords_form
    #метод пост работать без этой строчки не будет. Защита от хакерства
    args.update(csrf(request))
    #проверка условия, если наш запрос пост, то переменной name присвоим некоторое значение этой формы
    if request.method == 'POST':
        key = request.POST.get('name', '')
        args['key_name'] = key
        #получим статьи по фильтру(использет точное совпадение - строка поиска должна полностью схожа с результатом)
        args['articles'] = Article.objects.filter(keywords__name__exact=key)
        #если какие-то статьи существуют, то выведем по ним инфу, иначе страницу о том что их нет

        if args['articles']:
            return  render_to_response('keywpage.html', args, RequestContext(request))
        else:
            return render_to_response('keywpage_no.html', args, RequestContext(request))

    #вывод, если запрос не пост
    else:
        return redirect(return_path)

#Выберем все статьи, которые имеют выбранный тег
def cloudtegs(request, id):

    args = {}
    args['cloudtegs'] = Cloudtegs.objects.all()
    #конкретный тег по нашему id
    args['cloud_s'] = Cloudtegs.objects.get(id=id)
    #статьи, фильтр который по статьям имеет точное совпадение. Данная строка фильтра связывает 2 поля: keywords и name
    args['articles'] = Article.objects.filter(cloudtegs__name__exact=args['cloud_s'])
    #Данная переменная нужна для того чтобы на данной странице отобразить дерево категорий
    args['projects'] = Category.objects.all()
    args['username'] = auth.get_user(request).username
    return render(request, 'cloudpage.html', args)

def addlike(request, article_id):

    try:
        if article_id in request.COOKIES:
            return_path=request.META.get('HTTP_REFERER', '/')
            return redirect(return_path)

        else:
            article = Article.objects.get(id=article_id)
            article.article_likes += 1
            article.save()
            return_path = request.META.get('HTTP_REFERER', '/')
            response = redirect(return_path)
            response.set_cookie(article_id, "test")
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')



def article_cat(request, category_id=1):
    # связь с формой
    keywords_form = KeywordsForm
    args={}
    args['projects'] = Category.objects.all()
    args['category'] = Category.objects.get(id=category_id)
    args['articles'] = Article.objects.filter(article_category=category_id)
    args['username'] = auth.get_user(request).username
    #Отображает страницы по категории
    args['keywords'] = Keywords.objects.all()
    args['cloudtegs'] = Cloudtegs.objects.all()
    # реализация выдачи всех дочерних категорий, категория полученная из запроса.
    # из нее получаем всех наследников. Раньше была article, а теперь category_articles.
    # В шаблоне article_cat тоже необходимо ввести изменения
    branch_categories = args['category'].get_descendants(include_self=True)
    args['category_articles'] = Article.objects.filter(article_category__in=branch_categories).distinct()
    args['form_keywords'] = keywords_form
    return render_to_response('article_cat.html', args)






#выбор всех статей, которые имеют выбранного автора
def authors(request, id):
    # связь с формой
    keywords_form = KeywordsForm
    args = {}
    args['form_keywords'] = keywords_form
    args['authors'] = Author.objects.all()
    # конкретный  по нашему id
    args['author_s'] = Author.objects.get(id=id)
    args['articles'] = Article.objects.filter( article_author__name__exact=args['author_s'])
    args['projects'] = Category.objects.all()
    args['username'] = auth.get_user(request).username

    return render(request, 'author_page.html', args)

def home(request):
    # связь с формой
    keywords_form = KeywordsForm
    args = {}
    args['articles'] = Article.objects.all()
    args['authors'] = Author.objects.all()
    args['projects'] = Category.objects.all()
    args['username'] = auth.get_user(request).username
    args['homes'] = Home.objects.all()
    args['form_keywords'] = keywords_form
    return render(request, 'home.html', args)






