from django.db import models
from django.utils.text import slugify
from solo.models import SingletonModel


def generate_unique_slug(instance, source_field, slug_field):
    """
    Генерирует уникальный slug для instance на основе значения source_field.
    Если slug уже существует у другой записи — добавляет -1, -2, -3 ...
    instance: объект модели (self)
    source_field: имя поля-источника, например 'name' или 'title'
    slug_field: имя slug-поля, например 'slug' или 'slugfilter'
    """
    source_value = getattr(instance, source_field)
    base_slug = slugify(source_value) or 'item'
    slug = base_slug
    ModelClass = instance.__class__

    counter = 1
    while ModelClass.objects.filter(**{slug_field: slug}).exclude(pk=instance.pk).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    return slug


class Base(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Назва'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='URL-адреса (slug)'
    )
    about = models.TextField(
        max_length=512,
        verbose_name='Опис'
    )
    weight = models.IntegerField(
        verbose_name='Вага, г'
    )
    price = models.IntegerField(
        verbose_name='Ціна, грн'
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубліковано на сайті'
    )
    like = models.IntegerField(
        default=0,
        verbose_name='Кількість вподобань'
    )
    category = models.ForeignKey(
        'Filter',
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категорія'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)

    @property
    def main_image(self):
        """Главное фото товара: сначала ищем is_main=True, иначе первое по sort_order."""
        images = list(self.images.all())
        if not images:
            return None
        for img in images:
            if img.is_main:
                return img
        return images[0]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Каталог товарів'
        ordering = ['-id']


class Filter(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Назва'
    )
    slugfilter = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='URL-адреса (slug)'
    )

    def save(self, *args, **kwargs):
        if not self.slugfilter:
            self.slugfilter = generate_unique_slug(self, 'title', 'slugfilter')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорія товарів'
        verbose_name_plural = 'Категорії товарів'
        ordering = ['title']


class About(SingletonModel):
    about = models.TextField(
        verbose_name='Текст блоку "Про нас"'
    )

    instagram_url = models.URLField(
        blank=True,
        default='https://www.instagram.com/the28street/',
        verbose_name='Посилання на Instagram'
    )
    instagram_post_url = models.URLField(
        blank=True,
        verbose_name='Посилання на пост Instagram для вбудови на сторінці "Про нас"'
    )

    stat1_value = models.CharField(max_length=20, blank=True, verbose_name='Цифра 1 (напр. "2021")')
    stat1_label = models.CharField(max_length=60, blank=True, verbose_name='Підпис 1 (напр. "рік заснування")')
    stat2_value = models.CharField(max_length=20, blank=True, verbose_name='Цифра 2 (напр. "500+")')
    stat2_label = models.CharField(max_length=60, blank=True, verbose_name='Підпис 2')
    stat3_value = models.CharField(max_length=20, blank=True, verbose_name='Цифра 3 (напр. "4.9")')
    stat3_label = models.CharField(max_length=60, blank=True, verbose_name='Підпис 3')

    feature1_title = models.CharField(max_length=60, blank=True, verbose_name='Заголовок переваги 1')
    feature1_text = models.CharField(max_length=200, blank=True, verbose_name='Текст переваги 1')
    feature2_title = models.CharField(max_length=60, blank=True, verbose_name='Заголовок переваги 2')
    feature2_text = models.CharField(max_length=200, blank=True, verbose_name='Текст переваги 2')
    feature3_title = models.CharField(max_length=60, blank=True, verbose_name='Заголовок переваги 3')
    feature3_text = models.CharField(max_length=200, blank=True, verbose_name='Текст переваги 3')

    aboutPhoto1 = models.ImageField(upload_to='uploads/images/', blank=True, null=True,
                                    verbose_name='Фото на сторінці "Про нас" 1')
    aboutPhoto2 = models.ImageField(upload_to='uploads/images/', blank=True, null=True,
                                    verbose_name='Фото на сторінці "Про нас" 2')

    imgSlider1 = models.ImageField(upload_to='uploads/images/', verbose_name='Слайдер (ПК), фото 1', blank=True,
                                   null=True)
    videoSlider1 = models.FileField(upload_to='uploads/videos/',
                                    verbose_name='Слайдер (ПК), відео 1 (пріоритетне над фото)', blank=True, null=True)
    imgSlider2 = models.ImageField(upload_to='uploads/images/', verbose_name='Слайдер (ПК), фото 2', blank=True,
                                   null=True)
    videoSlider2 = models.FileField(upload_to='uploads/videos/',
                                    verbose_name='Слайдер (ПК), відео 2 (пріоритетне над фото)', blank=True, null=True)
    imgSlider3 = models.ImageField(upload_to='uploads/images/', verbose_name='Слайдер (ПК), фото 3', blank=True,
                                   null=True)
    videoSlider3 = models.FileField(upload_to='uploads/videos/',
                                    verbose_name='Слайдер (ПК), відео 3 (пріоритетне над фото)', blank=True, null=True)

    def __str__(self):
        return 'Інформація сайту'

    class Meta:
        verbose_name = 'Інформація сайту'
        verbose_name_plural = 'Інформація сайту'


class GalleryCategory(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Назва'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='URL-адреса (slug)'
    )

    image = models.ImageField(
        upload_to='uploads/gallery/categories/',
        verbose_name='Основне зображення'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Показувати на сайті'
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок відображення'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорія галереї'
        verbose_name_plural = 'Категорії галереї'
        ordering = ['sort_order', 'title']


class Gallery(models.Model):
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.CASCADE,
        related_name='galleries',
        verbose_name='Категорія галереї'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Назва альбому'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='URL-адреса (slug)'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Показувати на сайті'
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок відображення'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Альбом галереї'
        verbose_name_plural = 'Альбоми галереї'
        ordering = ['sort_order', 'title']


class GalleryImage(models.Model):
    gallery = models.ForeignKey(
        Gallery,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Альбом'
    )
    image = models.ImageField(
        upload_to='uploads/gallery/images/',
        verbose_name='Фото'
    )
    alt_text = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Опис фото (для SEO)'
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок відображення'
    )

    def __str__(self):
        return f'Фото для альбому: {self.gallery.title}'

    class Meta:
        verbose_name = 'Фото галереї'
        verbose_name_plural = 'Фото галереї'
        ordering = ['sort_order', 'id']


class BaseImage(models.Model):
    """Фото товару. Один товар -> багато фото (замінює старі image1/image2/image3)."""
    product = models.ForeignKey(
        Base,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='uploads/images/',
        verbose_name='Фото'
    )

    is_main = models.BooleanField(
        default=False,
        verbose_name='Головне фото товару'
    )

    def __str__(self):
        return f'Фото товару: {self.product.name}'

    class Meta:
        verbose_name = 'Фото товару'
        verbose_name_plural = 'Фото товарів'
        ordering = ['id']

