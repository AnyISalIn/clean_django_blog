from django import forms
from django.conf import settings
from tag.models import Tag
from .models import Article
from .tools import delete_no_article_tag, get_field_attrs


class MyTagField(forms.MultipleChoiceField):
    widget = forms.TextInput(get_field_attrs('Tags'))

    def clean(self, value):
        return value


class ArticleForm(forms.ModelForm):
    tag_list = MyTagField(required=False)

    class Meta:
        model = Article
        fields = ('title', 'background', 'tag_list', 'description', 'raw_content',)
        widgets = {
            'title': forms.TextInput(get_field_attrs('Title')),
            'background': forms.TextInput(get_field_attrs('Background Url, default {}'.format(
                settings.CLEAN_BLOG_CONFIG.get('SITE_ARTICLE_BACKGROUND')))),
            'description': forms.TextInput(get_field_attrs('Description')),
            'raw_content': forms.Textarea(get_field_attrs('Markdown Content', textarea=True))
        }

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.initial['tag_list'] = ','.join([t.name for t in Tag.objects.filter(article=self.instance).all()])
        self.fields['background'].required = False

    def clean_tag_list(self):
        tags = self.cleaned_data.get('tag_list') or []
        if tags:
            if ' ' in tags:
                raise forms.ValidationError('只能通过 , 分隔多个标签(不能包含空格)')
            return tags.split(',')
        return tags

    def save(self, commit=True):
        article = super(ArticleForm, self).save()
        tags = self.cleaned_data.get('tag_list')
        if tags:
            remove_tags = [t for t in article.tags.all() if t.name not in tags]
            article.tags.remove(*remove_tags)
            delete_no_article_tag(remove_tags)
            for item in tags:
                tag = Tag.objects.filter(name=item).first()
                if not tag:
                    tag = Tag.objects.create(name=item)
                article.tags.add(tag)
        else:
            remove_tags = article.tags.all()
            article.tags.remove(*remove_tags)  # remove all tags, if tag_list is empty
            delete_no_article_tag(remove_tags)
        return article
