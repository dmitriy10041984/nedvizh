from django.forms import ModelForm
from article.models import Comments, Keywords


class CommentForm(ModelForm):

    class Meta:
        model = Comments
        fields = ['comments_text']

class KeywordsForm(ModelForm):

    class Meta:
        model = Keywords
        fields = ['name']