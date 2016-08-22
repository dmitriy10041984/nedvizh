import mptt
from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_model
from embed_video.fields import EmbedVideoField
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Home(models.Model):
    home_title = models.CharField(null=True, blank=True, max_length=200)
    home_text = tinymce_model.HTMLField(null=True, blank=True)
    #поле необязательное
    home_image = models.ImageField(null=True, blank=True, upload_to="images/", verbose_name="Изображения")
    home_video = EmbedVideoField(null=True, blank= True, verbose_name="Видео")
    home_date = models.DateTimeField(null=True, blank=True)

    class Meta():
        db_table = 'home'
        ordering = ['home_date']
        verbose_name = "Главная страница"
        verbose_name_plural = "Статические страницы"

    def __str__(self):
        return self.home_title

    def bit_home(self):
        if self.home_image:
            return u'<img src="%s" width="50px">' % self.home_image.url
        else:
            return "Нет изображения"

    bit_home.short_desription= "Изображение"
    bit_home.allow_tags = True


class Author(models.Model):
    name = models.CharField(max_length=150, verbose_name="Риелтор")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    author_image = models.ImageField(null=True, blank=True, upload_to="images/", verbose_name="Фотография риелтора")

    class Meta():
        db_table = "author"
        verbose_name = "Риелтор"
        verbose_name_plural = "Риелторы"

    def __str__(self):
        return self.name

    def bit_author(self):
        if self.author_image:
            return u'<img src="%s" width="50px">' % self.author_image.url
        else:
            return "Нет изображения"

    bit_author.short_desription = "Изображение"
    bit_author.allow_tags = True







#Необходимо писать облако тегов до всех остальных классов
class Keywords(models.Model):

    name = models.CharField(max_length=50, unique=True, verbose_name='Кто ищет - тот всегда найдет')

    class Meta():
        db_table = 'keywords'
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"

    def __str__(self):
        return self.name

#Необходимо писать облако тегов до всех остальных классов
class Cloudtegs(models.Model):

    class Meta():
        db_table = 'cloudtegs'
        verbose_name = "тег"
        verbose_name_plural = "Облако тегов"

    name = models.CharField(max_length=50, unique=True, verbose_name='Теги')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Category(MPTTModel):

    class Meta():
        db_table = 'category'
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ('tree_id', 'level')

    name = models.CharField(max_length=150, verbose_name='Категория')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name='Родительский класс')

    def __str__(self):
        return self.name

    #строит структуру name в виде дерева
    class MPTTMeta:
        order_insertion_by = ['name']


mptt.register(Category, order_insertion_by = ['name'])




class Article(models.Model):
    article_title = models.CharField(max_length=200)
    #поле необязательное
    article_image = models.ImageField(null=True, blank=True, upload_to="images/", verbose_name="Изображения")
    #необязательная
    article_video = EmbedVideoField(null=True, blank= True, verbose_name="Видео")
    article_text_min = tinymce_model.HTMLField(verbose_name="Краткое описание")
    article_text = tinymce_model.HTMLField(verbose_name="Подробное описание")
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default=0)
    #связка деревобразного строения со статьями
    article_category = TreeForeignKey(Category, blank=True, null=True, related_name='cat')
    #связка с автором
    article_author = models.ForeignKey(Author, max_length=150, verbose_name="Риелтор")
    #Пропишем поле, которое свяжет keywords, с данным классом
    keywords = models.ManyToManyField(Keywords, related_name='keywords', related_query_name='keyword', verbose_name='Ключевые слова поиска')
    #Пропишем поле, которое свяжет cloudtegs, с данным классом
    cloudtegs = models.ManyToManyField(Cloudtegs, related_name='cloudtegs', related_query_name='cloudteg', verbose_name='Ключевые слова')
    article_main_data = tinymce_model.HTMLField(verbose_name="Главное о недвижимости")
    article_address = tinymce_model.HTMLField(verbose_name="Адрес")


    class Meta():
        db_table = 'article'
        ordering = ['article_title']
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"

    def __str__(self):
        return self.article_title

    def bit(self):
        if self.article_image:
            return u'<img src="%s" width="50px">' % self.article_image.url
        else:
            return "Нет изображения"

    bit.short_desription= "Изображение"
    bit.allow_tags = True


class Comments(models.Model):

    comments_article = models.ForeignKey(Article)
    comments_text = models.TextField(verbose_name="Текст комментария")
    comments_date = models.DateField(u'date', auto_now=True)
    comments_author = models.ForeignKey(User)

    class Meta():
        db_table = 'comments'
        ordering = ['comments_article']
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.comments_article




