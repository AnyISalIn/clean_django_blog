from django.conf import settings


def site_info(request):
    return settings.CLEAN_BLOG_CONFIG
