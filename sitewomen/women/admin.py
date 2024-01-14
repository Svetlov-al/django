from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from women.models import Category, TagPost, Women


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус Женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужм')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husbund__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husbund__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'photo', 'post_photo', 'cat', 'husbund', 'slug', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['post_photo']
    filter_horizontal = ['tags']
    list_display = ['title', 'post_photo', 'time_create', 'is_published', 'cat']
    list_display_links = ['title', 'post_photo']
    ordering = ['time_create']
    list_editable = ['is_published']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']
    save_on_top = True

    list_per_page = 10

    actions = ['set_published', 'set_draft']

    @admin.display(description='Фотография')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return 'Без фото'

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, woman: Women):
        return f"Описание {len(woman.content)} символов."

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} записей.")

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} записей.", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag', 'slug']
    list_display_links = ['id', 'tag', 'slug']
