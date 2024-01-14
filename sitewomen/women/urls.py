from django.urls import path, register_converter
from django.views.decorators.cache import cache_page
from . import converters
from . import views

register_converter(converters.FourDigityearConverter, "year4")

urlpatterns = [
    path('', cache_page(30)(views.WomenHome.as_view()), name='home'),
    path('about/', views.ContactFormView.as_view(), name='about'),
    path('add_page/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.WomenTags.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<int:pk>', views.DeletePage.as_view(), name='delete_page'),
]
