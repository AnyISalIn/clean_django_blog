# Clean Django Blog

> based on [startbootstrap clean blog](https://github.com/BlackrockDigital/startbootstrap-clean-blog)

## Demo

[online demo on heroku](https://shrouded-atoll-58336.herokuapp.com/)

![home](https://o7mt5n76t.qnssl.com/clean_django_blog_home.png)
![tag](https://o7mt5n76t.qnssl.com/clean_django_blog_tag.png)
![detail](https://o7mt5n76t.qnssl.com/clean_django_blog_detail.png)
![editor](https://o7mt5n76t.qnssl.com/clean_django_blog_editor.png)

## Quick Start

```shell
$ ./deploy.sh

$ export SITE_NAME='AnyISalIn Blog' # set blog name

$ export SITE_DESCRIPTION='This is Description'

# start with gunicorn
$ gunicorn --bind 0.0.0.0:8000 clean_django_blog.wsgi:application
```

## Deploy On Heroku

```shell
$ heroku create

$ heroku config:set DISABLE_COLLECTSTATIC=1

$ git push heroku master

$ heroku config:set SITE_NAME='AnyISalIn Blog'

$ heroku config:set SITE_DESCRIPTION='This is Description'

$ heroku run python manage.py migrate

$ heroku ps:scale web=1

$ heroku open
```

## Config

```python
# settings.py

CLEAN_BLOG_CONFIG = {
    'SITE_NAME': os.getenv('SITE_NAME', 'Clean Blog'), # site name
    'SITE_DESCRIPTION': os.getenv('SITE_DESCRIPTION', 'Shared Your knowledge'), # site description
    'SITE_HOME_BACKGROUND': os.getenv('SITE_HOME_BACKGROUND', '/static/img/home-bg.png'), # default home page background
    'SITE_ARTICLE_BACKGROUND': os.getenv('SITE_POST_BACKGROUND', '/static/img/article-bg.png'), # default article page background
    'SITE_FORM_BACKGROUND': os.getenv('SITE_FORM_BACKGROUND', '/static/img/form-bg.png'), # default form page background
    'SITE_ERROR_BACKGROUND': os.getenv('SITE_ERROR_BACKGROUND', '/static/img/error-bg.png'), # default error page background
    'SITE_ZHIHU_URL': os.getenv('ZHIHU_URL', 'https://www.zhihu.com/'), # zhihu url
    'SITE_GITHUB_URL': os.getenv('GITHUB_URL', 'https://github.com/anyisalin') # github url
}
```
