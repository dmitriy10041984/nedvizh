from mptt.admin import MPTTModelAdmin

from django.contrib import admin

# Register your models here.
from article.models import Article, Comments, Category, Keywords, Cloudtegs
from article.models import Home, Author

# Register your models here.
#для статей
class ArticleInline(admin.StackedInline):
    model = Comments
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    fields = ['article_title', 'article_category', 'article_main_data', 'article_address', 'article_text', 'article_date', 'article_image', 'article_video', 'keywords', 'cloudtegs', 'article_author', 'article_text_min']
    inlines = [ArticleInline]
    list_filter = ['article_category']
    list_display = ('article_title', 'article_category', 'article_date', 'article_image', 'bit')
    search_fields = ['article_title']

    class Media:
        js = (
            '/static/tiny_mce/tiny_mce.js',
            '/static/tiny_mce/tiny_mce_init.js',
        )


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'parent']


class KeywordsAdmin(admin.ModelAdmin):
    fields = ['name']


class CloudtegsAdmin(admin.ModelAdmin):
    fields = ['name']

#для страниц
class HomeAdmin(admin.ModelAdmin):
    fields = ['home_title', 'home_text', 'home_date', 'home_image', 'home_video']
    list_filter = ['home_title']
    list_display = ('home_title', 'home_text', 'home_date', 'home_image', 'home_video', 'bit_home')
    search_fields = ['home_title']


class AuthorAdmin(admin.ModelAdmin):
    fields = ['name', 'phone', 'author_image']
    list_filter = ['name']
    list_display = ('name', 'phone', 'author_image', 'bit_author')
    search_fields = ['name']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(Home, HomeAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Cloudtegs, CloudtegsAdmin)

