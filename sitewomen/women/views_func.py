from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddPostForm, UploadFileForm
from .models import Category, TagPost, UploadFiles, Women

menu = [{"title": "О сайте", "url_name": "about"},
        {"title": "Добавить статью", "url_name": "add_page"},
        {"title": "Обратная связь", "url_name": "contact"},
        {"title": "Войти", "url_name": "login"}]


def index(request: HttpRequest):
    posts = Women.published.all().select_related('cat')
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": posts,
        "cat_selected": 0
    }
    return render(request, 'women/index.html', context=data)


# def handle_uploaded_file(file):
#     with open(f'uploads/{file.name}', 'wb+') as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)


def about(request):
    if request.POST:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    data = {
        "title": "О сайте",
        "menu": menu,
        "form": form
    }
    return render(request, 'women/about.html', data)


def add_page(request: HttpRequest):
    if request.POST:
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    data = {'menu': menu,
            'title': 'Добавление статьи',
            'form': form}
    return render(request, 'women/add_page.html', data)


def contact(request: HttpRequest):
    return HttpResponse("Обратная связь")


def login(request: HttpRequest):
    return HttpResponse("Войти")


def show_post(request: HttpRequest, post_slug: str):
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        "title": "Отображение по рубрикам",
        "menu": menu,
        "post": post,
        "cat_selected": 1
    }
    return render(request, 'women/post.html', context=data)


def show_category(request: HttpRequest, cat_slug: str):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": category.pk
    }
    return render(request, 'women/index.html', context=data)


def show_tag_postlist(request: HttpRequest, tag_slug: str):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

    data = {
        "title": f"Тэг: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None
    }
    return render(request, 'women/index.html', context=data)


def page_not_found(requset, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
