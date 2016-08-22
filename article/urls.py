from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


from article import views

urlpatterns = [
    url(r'^1/', views.basic_one),
    url(r'^2/', views.template_two),
    url(r'^3/', views.template_three_simple),
    url(r'^articles/all/$', views.articles),
    url(r'^articles/get/(?P<article_id>\d+)/$', views.article),
    url(r'^articles/addlike/(?P<article_id>\d+)/$', views.addlike),
    url(r'^articles/addcomment/(?P<article_id>\d+)/$', views.addcomment),
    url(r'^page/(\d+)/$', views.articles),
    url(r'^$', views.articles, name='/'),
    url(r'^category/get/(?P<category_id>\d+)/$', views.article_cat),
    #облако тегов
    url(r'^cloudteg/(?P<id>\d+)/$', views.cloudtegs),
    url(r'^keyword/$', views.keywords),
    url(r'^author/(?P<id>\d+)/$', views.authors),
    url(r'^home/', views.home, name='home'),



]

#Если картинки не отображаются, на реальном сервере они отобразятся, необходимо указать
#если режим отладки, то должны использовать данную строку
if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()


""""

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'firstapp.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^1/', 'article.views.basic_one'),
                       url(r'^2/', 'article.views.template_two'),
                       url(r'^3/', 'article.views.template_three_simple'),
                       url(r'^articles/all/$', 'article.views.articles'),
                       url(r'^articles/get/(?P<article_id>\d+)/$', 'article.views.article'),
                       url(r'^articles/addlike/(?P<article_id>\d+)/$', 'article.views.addlike'),
                       url(r'^articles/addcomment/(?P<article_id>\d+)/$', 'article.views.addcomment'),
                       url(r'^page/(\d+)/$', 'article.views.articles'),
                       url(r'^', 'article.views.articles'),

                       )
"""