from django import template
from django.db.models import Count

from women.models import Category, TagPost

register = template.Library()



@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(count_posts=Count("posts")).filter(count_posts__gt=0)
    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag('women/list_tags.html')
def show_all_tags(cat_selected=0):
    tags = TagPost.objects.annotate(count_tags=Count('tags')).filter(count_tags__gt=0)
    return {"tags": tags}
