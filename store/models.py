from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    class PageType(models.TextChoices):
        CATALOG = 'catalog', 'Каталог товаров'
        DELIVERY = 'delivery', 'Доставка'
        PAYMENT = 'payment', 'Оплата'
        NEWS = 'news', 'Новости'
        PROMOTIONS = 'promotions', 'Акции'
        ABOUT = 'about', 'О нас'
        CART = 'cart', 'Корзина'

    title = models.CharField('Название пункта меню', max_length=100)
    page_type = models.CharField('Тип страницы', max_length=20, choices=PageType.choices, unique=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        mapping = {
            self.PageType.CATALOG: 'store:catalog',
            self.PageType.DELIVERY: 'store:info_page',
            self.PageType.PAYMENT: 'store:info_page',
            self.PageType.NEWS: 'store:news_list',
            self.PageType.PROMOTIONS: 'store:promotion_list',
            self.PageType.ABOUT: 'store:info_page',
            self.PageType.CART: 'store:cart',
        }
        if self.page_type in {self.PageType.DELIVERY, self.PageType.PAYMENT, self.PageType.ABOUT}:
            return reverse(mapping[self.page_type], kwargs={'page_type': self.page_type})
        return reverse(mapping[self.page_type])


class Category(models.Model):
    name = models.CharField('Название', max_length=120)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Описание', blank=True)
    image_url = models.URLField('Изображение', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField('Название', max_length=150)
    slug = models.SlugField('Slug', unique=True)
    short_description = models.CharField('Краткое описание', max_length=255)
    description = models.TextField('Полное описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField('Остаток', default=0)
    image_url = models.URLField('Изображение', blank=True)
    is_featured = models.BooleanField('Показывать в карусели', default=False)
    is_recommended = models.BooleanField('Рекомендуемый', default=False)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('store:product_detail', kwargs={'slug': self.slug})


class InfoPage(models.Model):
    class PageType(models.TextChoices):
        DELIVERY = 'delivery', 'Доставка'
        PAYMENT = 'payment', 'Оплата'
        ABOUT = 'about', 'О нас'

    page_type = models.CharField('Тип страницы', max_length=20, choices=PageType.choices, unique=True)
    title = models.CharField('Заголовок', max_length=150)
    hero_title = models.CharField('Hero-заголовок', max_length=150)
    hero_subtitle = models.CharField('Hero-подзаголовок', max_length=255)
    content = models.TextField('Контент')

    class Meta:
        verbose_name = 'Информационная страница'
        verbose_name_plural = 'Информационные страницы'

    def __str__(self) -> str:
        return self.title


class NewsArticle(models.Model):
    title = models.CharField('Заголовок', max_length=150)
    slug = models.SlugField('Slug', unique=True)
    summary = models.CharField('Краткое описание', max_length=255)
    content = models.TextField('Контент')
    image_url = models.URLField('Изображение', blank=True)
    published_at = models.DateField('Дата публикации')
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return self.title


class Promotion(models.Model):
    title = models.CharField('Заголовок', max_length=150)
    slug = models.SlugField('Slug', unique=True)
    summary = models.CharField('Краткое описание', max_length=255)
    content = models.TextField('Контент')
    discount_label = models.CharField('Метка скидки', max_length=50)
    image_url = models.URLField('Изображение', blank=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateField('Дата создания')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self) -> str:
        return self.title
