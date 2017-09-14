from django import forms
from django.conf import settings
from tag.models import Tag
from .models import Article
from .tools import delete_no_article_tag, get_field_attrs


class MyTagField(forms.Field):
    '''由于前端需要 TextInput 的输出框，但是数据又不需要做任何处理，所以单独定义一个 Field'''
    widget = forms.TextInput(get_field_attrs('Tags'))

    def clean(self, value):
        return value


class ArticleForm(forms.ModelForm):
    '''Article Form 用于修改/新建文章'''
    tag_list = MyTagField(required=False) # 由于 tags 是 ManyToMany 的关系，不能直接写在 fields/widgets 里面，需要单独拿出来处理

    class Meta:
        model = Article
        fields = ('title', 'background', 'tag_list', 'description', 'raw_content',) # 这个表单的所有 Field
        widgets = {
            'title': forms.TextInput(get_field_attrs('Title')),
            'background': forms.TextInput(get_field_attrs('Background Url, default {}'.format(
                settings.CLEAN_BLOG_CONFIG.get('SITE_ARTICLE_BACKGROUND')))),
            'description': forms.TextInput(get_field_attrs('Description')),
            'raw_content': forms.Textarea(get_field_attrs('Markdown Content', textarea=True))
        }

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.initial['tag_list'] = ','.join([t.name for t in Tag.objects.filter(article=self.instance).all()]) # 初始值为当前文章的所有 Tag
        self.fields['background'].required = False

    def clean_tag_list(self):
        '''处理 tag_list 的数据，前端传过来应该是 python,web,django 这样的，要将他变成 ['python', 'web', 'django']'''
        tags = self.cleaned_data.get('tag_list') or []
        if tags:
            if ' ' in tags:
                raise forms.ValidationError('multi tag like "python,django"(Cannot contain Spaces)')
            return tags.split(',')
        return tags

    def save(self, commit=True):
        '''重写 save 方法，文章保存后做一些和 tag 有关的操作'''
        article = super(ArticleForm, self).save()
        tags = self.cleaned_data.get('tag_list') # 获取处理过后的 tag，经过 clean_tag_list 处理后应该是类似 ['python', 'web', 'django'] 的列表 或者为一个空列表
        if tags: # 如果 tags 不为空
            remove_tags = [t for t in article.tags.all() if t.name not in tags] # 首先列出将要删掉的Tag
            '''
            比如 <Python Django Web 开发> 这篇文章原本有 ['python', 'web', 'django'] 这几个 Tag
            但是这次前端只传递过来 ['web', 'django']，将 python 这个标签删了，所以 remove_tags 应该就是 ['python']
            '''
            article.tags.remove(*remove_tags) # 删除文章 tags 里面相应标签
            delete_no_article_tag(remove_tags) # 清理没有文章的标签，比如说 python 这个标签下只有 <Python Django Web 开发> 这一篇文章，但是这篇文章把 python 这个标签删除了，那么 python 这个标签就没有文章了，应该删除
            for item in tags:
                '''
                如果标签存在，添加对应文章中
                如果不存在，先创建标签，再添加到文章中
                '''
                tag = Tag.objects.filter(name=item).first()
                if not tag:
                    tag = Tag.objects.create(name=item)
                article.tags.add(tag)
        else:
            '''
            如果 tags 为空，那么将要删除这篇文章的所有标签
            '''
            remove_tags = article.tags.all()
            article.tags.remove(*remove_tags)  # remove all tags, if tag_list is empty
            delete_no_article_tag(remove_tags)
        return article
