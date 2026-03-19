from datetime import date

from django.db import migrations


def seed_store(apps, schema_editor):
    MenuItem = apps.get_model('store', 'MenuItem')
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')
    InfoPage = apps.get_model('store', 'InfoPage')
    NewsArticle = apps.get_model('store', 'NewsArticle')
    Promotion = apps.get_model('store', 'Promotion')

    menu = [
        ('Каталог товаров', 'catalog', 1),
        ('Доставка', 'delivery', 2),
        ('Оплата', 'payment', 3),
        ('Новости', 'news', 4),
        ('Акции', 'promotions', 5),
        ('О нас', 'about', 6),
        ('Корзина', 'cart', 7),
    ]
    for title, page_type, order in menu:
        MenuItem.objects.get_or_create(page_type=page_type, defaults={'title': title, 'order': order})

    categories = {
        'smartfony': Category.objects.get_or_create(
            slug='smartfony',
            defaults={
                'name': 'Смартфоны',
                'description': 'Современные смартфоны для работы и отдыха.',
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80',
            },
        )[0],
        'noutbuki': Category.objects.get_or_create(
            slug='noutbuki',
            defaults={
                'name': 'Ноутбуки',
                'description': 'Производительные решения для офиса и дома.',
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80',
            },
        )[0],
        'aksessuary': Category.objects.get_or_create(
            slug='aksessuary',
            defaults={
                'name': 'Аксессуары',
                'description': 'Полезные аксессуары и гаджеты.',
                'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=900&q=80',
            },
        )[0],
    }

    products = [
        ('treidpro-x1', 'TreidPro X1', 'Флагманский смартфон с ярким OLED-дисплеем.', 'Смартфон с тройной камерой, eSIM и быстрой зарядкой.', '79990.00', 15, categories['smartfony'], True, True, 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1200&q=80'),
        ('treidbook-air', 'TreidBook Air', 'Лёгкий ноутбук для бизнеса и учебы.', 'Ультрабук с металлическим корпусом и батареей на весь день.', '109990.00', 8, categories['noutbuki'], True, True, 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=1200&q=80'),
        ('treidpods-pro', 'TreidPods Pro', 'Беспроводные наушники с шумоподавлением.', 'Наушники с прозрачным режимом и объёмным звучанием.', '14990.00', 42, categories['aksessuary'], True, True, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=80'),
        ('treidwatch-s', 'TreidWatch S', 'Умные часы для спорта и уведомлений.', 'AMOLED-экран, GPS и анализ активности в течение дня.', '19990.00', 30, categories['aksessuary'], False, True, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1200&q=80'),
        ('treidpro-tab', 'TreidPro Tab', 'Планшет для работы, чтения и развлечений.', 'Большой экран, стилус и поддержка клавиатуры.', '45990.00', 14, categories['smartfony'], False, True, 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=1200&q=80'),
        ('treidhub-7', 'TreidHub 7-in-1', 'USB-C хаб для ноутбука.', 'HDMI, кардридер и дополнительные порты в одном корпусе.', '6990.00', 65, categories['aksessuary'], False, False, 'https://images.unsplash.com/photo-1587033411391-5d9e51cce126?auto=format&fit=crop&w=1200&q=80'),
    ]
    for slug, name, short_description, description, price, stock, category, is_featured, is_recommended, image_url in products:
        Product.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'short_description': short_description,
                'description': description,
                'price': price,
                'stock': stock,
                'category': category,
                'is_featured': is_featured,
                'is_recommended': is_recommended,
                'image_url': image_url,
            },
        )

    pages = [
        ('delivery', 'Доставка', 'Быстрая доставка по всей России', 'Выберите удобный способ получения заказа.', 'Мы доставляем курьером, в пункты выдачи и транспортными компаниями. Средний срок обработки заказа — 15 минут, а отправка возможна в день оформления.'),
        ('payment', 'Оплата', 'Гибкие варианты оплаты', 'Оплачивайте заказ так, как удобно именно вам.', 'Доступна оплата банковской картой, по счёту для юридических лиц, через СБП и при получении. Все платежи проходят через защищённые шлюзы.'),
        ('about', 'О нас', 'TreidPro — магазин технологичных решений', 'Помогаем подобрать технику для работы и жизни.', 'Мы собрали каталог популярных устройств, аксессуаров и сервисов. Команда консультантов помогает подобрать технику, а администратор сайта может управлять контентом через встроенную панель Django Admin.'),
    ]
    for page_type, title, hero_title, hero_subtitle, content in pages:
        InfoPage.objects.get_or_create(
            page_type=page_type,
            defaults={'title': title, 'hero_title': hero_title, 'hero_subtitle': hero_subtitle, 'content': content},
        )

    news_items = [
        ('otkrytie-showroom', 'Открытие нового шоурума', 'Мы открыли новый шоурум с зоной тестирования техники.', 'В новом пространстве можно протестировать ноутбуки, смартфоны и аксессуары перед покупкой.', date(2026, 3, 12), 'https://images.unsplash.com/photo-1556740738-b6a63e27c4df?auto=format&fit=crop&w=1200&q=80'),
        ('vesennie-obnovleniya', 'Весенние обновления ассортимента', 'В каталог добавлены новые устройства и аксессуары.', 'В марте 2026 года в магазине появились ультрабуки, умные часы и новые линейки аксессуаров.', date(2026, 3, 5), 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80'),
        ('programma-loyalnosti', 'Запуск программы лояльности', 'Накопительные бонусы теперь доступны всем покупателям.', 'За каждый заказ начисляются бонусы, которые можно потратить на последующие покупки.', date(2026, 2, 20), 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1200&q=80'),
    ]
    for slug, title, summary, content, published_at, image_url in news_items:
        NewsArticle.objects.get_or_create(
            slug=slug,
            defaults={'title': title, 'summary': summary, 'content': content, 'published_at': published_at, 'image_url': image_url},
        )

    promotion_items = [
        ('smart-sale', 'Скидки на смартфоны', 'До -15% на флагманские модели.', 'Успейте приобрести смартфоны с расширенной гарантией и выгодной скидкой.', '-15%', date(2026, 3, 10), 'https://images.unsplash.com/photo-1556656793-08538906a9f8?auto=format&fit=crop&w=1200&q=80'),
        ('notebook-week', 'Неделя ноутбуков', 'Подарки при покупке ноутбуков.', 'При заказе ноутбука вы получаете фирменную сумку и беспроводную мышь.', 'Подарок', date(2026, 3, 1), 'https://images.unsplash.com/photo-1517336714739-489689fd1ca8?auto=format&fit=crop&w=1200&q=80'),
        ('accessory-bundle', 'Набор аксессуаров выгоднее', 'Комплектуйте покупки с выгодой до 20%.', 'При покупке наушников, часов и зарядки предоставляется специальная bundle-цена.', '-20%', date(2026, 2, 18), 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=1200&q=80'),
    ]
    for slug, title, summary, content, discount_label, created_at, image_url in promotion_items:
        Promotion.objects.get_or_create(
            slug=slug,
            defaults={'title': title, 'summary': summary, 'content': content, 'discount_label': discount_label, 'created_at': created_at, 'image_url': image_url},
        )


def unseed_store(apps, schema_editor):
    apps.get_model('store', 'Product').objects.all().delete()
    apps.get_model('store', 'Category').objects.all().delete()
    apps.get_model('store', 'InfoPage').objects.all().delete()
    apps.get_model('store', 'NewsArticle').objects.all().delete()
    apps.get_model('store', 'Promotion').objects.all().delete()
    apps.get_model('store', 'MenuItem').objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [('store', '0001_initial')]

    operations = [migrations.RunPython(seed_store, unseed_store)]
