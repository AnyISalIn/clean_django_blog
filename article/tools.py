from django.conf import settings


def delete_no_article_tag(tags):
    for t in tags:
        if not t.article_set.count():
            t.delete()


def get_field_attrs(placeholder, textarea=False):
    ret = {'class': 'form-control', 'placeholder': placeholder}
    if textarea:
        ret.update({'rows': 20})
    return ret


def get_config(key):
    return settings.CLEAN_BLOG_CONFIG.get(key)


def get_article_background():
    return get_config('SITE_ARTICLE_BACKGROUND')
