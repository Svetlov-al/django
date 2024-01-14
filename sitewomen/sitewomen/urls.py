from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from sitewomen import settings
from women.sitemaps import CategorySiteMap, PostSiteMap
from women.views import page_not_found

sitemaps = {
    'posts': PostSiteMap,
    'category': CategorySiteMap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml', cache_page(600)(sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found

admin.site.site_header = 'Админ панель'
admin.site.index_title = 'Известные женщины мира'
