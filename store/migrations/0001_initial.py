from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image_url', models.URLField(blank=True, verbose_name='Изображение')),
            ],
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.CreateModel(
            name='InfoPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_type', models.CharField(choices=[('delivery', 'Доставка'), ('payment', 'Оплата'), ('about', 'О нас')], max_length=20, unique=True, verbose_name='Тип страницы')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('hero_title', models.CharField(max_length=150, verbose_name='Hero-заголовок')),
                ('hero_subtitle', models.CharField(max_length=255, verbose_name='Hero-подзаголовок')),
                ('content', models.TextField(verbose_name='Контент')),
            ],
            options={'verbose_name': 'Информационная страница', 'verbose_name_plural': 'Информационные страницы'},
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название пункта меню')),
                ('page_type', models.CharField(choices=[('catalog', 'Каталог товаров'), ('delivery', 'Доставка'), ('payment', 'Оплата'), ('news', 'Новости'), ('promotions', 'Акции'), ('about', 'О нас'), ('cart', 'Корзина')], max_length=20, unique=True, verbose_name='Тип страницы')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={'verbose_name': 'Пункт меню', 'verbose_name_plural': 'Пункты меню', 'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('summary', models.CharField(max_length=255, verbose_name='Краткое описание')),
                ('content', models.TextField(verbose_name='Контент')),
                ('image_url', models.URLField(blank=True, verbose_name='Изображение')),
                ('published_at', models.DateField(verbose_name='Дата публикации')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
            ],
            options={'verbose_name': 'Новость', 'verbose_name_plural': 'Новости', 'ordering': ['-published_at']},
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('summary', models.CharField(max_length=255, verbose_name='Краткое описание')),
                ('content', models.TextField(verbose_name='Контент')),
                ('discount_label', models.CharField(max_length=50, verbose_name='Метка скидки')),
                ('image_url', models.URLField(blank=True, verbose_name='Изображение')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('created_at', models.DateField(verbose_name='Дата создания')),
            ],
            options={'verbose_name': 'Акция', 'verbose_name_plural': 'Акции', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('short_description', models.CharField(max_length=255, verbose_name='Краткое описание')),
                ('description', models.TextField(verbose_name='Полное описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Остаток')),
                ('image_url', models.URLField(blank=True, verbose_name='Изображение')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Показывать в карусели')),
                ('is_recommended', models.BooleanField(default=False, verbose_name='Рекомендуемый')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.category', verbose_name='Категория')),
            ],
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары', 'ordering': ['-created_at']},
        ),
    ]
