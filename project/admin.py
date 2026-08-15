from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from .models import *


def image_preview(image, width=90):
    if image:
        return mark_safe(f'<img src="{image.url}" style="width:{width}px; height:auto; border-radius:6px;" />')
    return 'Немає фото'


def video_preview(video, width=160):
    if video:
        return mark_safe(
            f'<video src="{video.url}" style="width:{width}px; height:auto; border-radius:6px;" '
            f'muted loop controls></video>'
        )
    return 'Немає відео'


class BaseImageInline(admin.TabularInline):
    """Фото товару прямо на сторінці товару."""
    model = BaseImage
    extra = 1
    fields = (
        'image',
        'image_preview_admin',
        'is_main',
    )
    readonly_fields = ('image_preview_admin',)

    def image_preview_admin(self, obj):
        return image_preview(obj.image)
    image_preview_admin.short_description = 'Превʼю'


@admin.register(Base)
class BaseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'main_image_preview',
        'category',
        'price',
        'weight',
        'is_published',
        'like',
    )
    list_display_links = ('name', 'main_image_preview')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    search_fields = ('name', 'about')
    list_per_page = 25
    save_on_top = True
    exclude = ('slug',)
    inlines = [BaseImageInline]

    fieldsets = (
        ('Основна інформація', {
            'fields': (
                'name',
                'category',
                'about',
            )
        }),
        ('Ціна та характеристики', {
            'fields': (
                'price',
                'weight',
            )
        }),
        ('Публікація', {
            'fields': (
                'is_published',
                'like',
            )
        }),
    )

    def main_image_preview(self, obj):
        main = obj.images.filter(is_main=True).first() or obj.images.first()
        return image_preview(main.image if main else None)
    main_image_preview.short_description = 'Фото'


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    search_fields = ('title',)
    save_on_top = True
    exclude = ('slugfilter',)

    fieldsets = (
        ('Основна інформація', {
            'fields': (
                'title',
            )
        }),

    )


@admin.register(About)
class AboutAdmin(SingletonModelAdmin):
    save_on_top = True
    readonly_fields = (
        'slider1_preview',
        'slider2_preview',
        'slider3_preview',
        'photo1_preview',
        'photo2_preview',
    )

    fieldsets = (
        ('Текст блоку "Про нас"', {
            'fields': (
                'about',
            )
        }),
        ('Цифри (необов\'язково — не заповните, блок просто не покажеться)', {
            'fields': (
                ('stat1_value', 'stat1_label'),
                ('stat2_value', 'stat2_label'),
                ('stat3_value', 'stat3_label'),
            )
        }),
        ('Переваги (необов\'язково)', {
            'fields': (
                ('feature1_title', 'feature1_text'),
                ('feature2_title', 'feature2_text'),
                ('feature3_title', 'feature3_text'),
            )
        }),
        ('Фото та Instagram на сторінці "Про нас"', {
            'fields': (
                'aboutPhoto1',
                'photo1_preview',
                'aboutPhoto2',
                'photo2_preview',
                'instagram_post_url',
                'instagram_url',
            )
        }),
        ('Слайд 1 (ПК)', {
            'description': 'Якщо завантажено відео — на сайті показується саме воно, фото ігнорується.',
            'fields': (
                'imgSlider1',
                'videoSlider1',
                'slider1_preview',
            )
        }),
        ('Слайд 2 (ПК)', {
            'description': 'Якщо завантажено відео — на сайті показується саме воно, фото ігнорується.',
            'fields': (
                'imgSlider2',
                'videoSlider2',
                'slider2_preview',
            )
        }),
        ('Слайд 3 (ПК)', {
            'description': 'Якщо завантажено відео — на сайті показується саме воно, фото ігнорується.',
            'fields': (
                'imgSlider3',
                'videoSlider3',
                'slider3_preview',
            )
        }),
    )

    def slider1_preview(self, obj):
        if obj.videoSlider1:
            return video_preview(obj.videoSlider1)
        return image_preview(obj.imgSlider1)
    slider1_preview.short_description = 'Превʼю слайда 1'

    def slider2_preview(self, obj):
        if obj.videoSlider2:
            return video_preview(obj.videoSlider2)
        return image_preview(obj.imgSlider2)
    slider2_preview.short_description = 'Превʼю слайда 2'

    def slider3_preview(self, obj):
        if obj.videoSlider3:
            return video_preview(obj.videoSlider3)
        return image_preview(obj.imgSlider3)
    slider3_preview.short_description = 'Превʼю слайда 3'

    def photo1_preview(self, obj):
        return image_preview(obj.aboutPhoto1)
    photo1_preview.short_description = 'Превʼю фото 1'

    def photo2_preview(self, obj):
        return image_preview(obj.aboutPhoto2)
    photo2_preview.short_description = 'Превʼю фото 2'


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = (
        'image',
        'image_preview_admin',
        'alt_text',
        'sort_order',
    )
    readonly_fields = ('image_preview_admin',)

    def image_preview_admin(self, obj):
        return image_preview(obj.image)
    image_preview_admin.short_description = 'Превʼю фото'


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'main_image_preview',
        'is_active',
        'sort_order',
    )
    list_editable = (
        'is_active',
        'sort_order',
    )
    search_fields = ('title',)
    save_on_top = True
    readonly_fields = (
        'main_image_preview',
    )
    exclude = ('slug',)

    fieldsets = (
        ('Основна інформація', {
            'fields': (
                'title',
                'is_active',
                'sort_order',
            )
        }),
        ('Зображення категорії', {
            'description': 'Перше зображення показується звичайно, друге — при наведенні курсора.',
            'fields': (
                'image',
                'main_image_preview',
            )
        }),
    )

    def main_image_preview(self, obj):
        return image_preview(obj.image)
    main_image_preview.short_description = 'Основне зображення'

    def hover_image_preview(self, obj):
        return image_preview(obj.hover_image)
    hover_image_preview.short_description = 'Зображення при наведенні'


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'is_active',
        'sort_order',
    )
    list_filter = (
        'category',
        'is_active',
    )
    list_editable = (
        'is_active',
        'sort_order',
    )
    search_fields = ('title',)
    save_on_top = True
    exclude = ('slug',)
    inlines = [GalleryImageInline]

    fieldsets = (
        ('Основна інформація альбому', {
            'fields': (
                'title',
                'category',
                'is_active',
                'sort_order',
            )
        }),
    )


try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.site_header = 'Адміністрування сайту'
admin.site.site_title = 'Адмін-панель'
admin.site.index_title = 'Керування контентом'