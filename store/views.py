from decimal import Decimal

from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, InfoPage, NewsArticle, Product, Promotion


class HomeView(TemplateView):
    template_name = 'store/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_ids = self.request.session.get('recently_viewed', [])[:8]
        recent_products = list(Product.objects.filter(id__in=recent_ids))
        recent_products.sort(key=lambda product: recent_ids.index(product.id))
        context.update(
            featured_products=Product.objects.filter(is_featured=True)[:6],
            recommended_products=Product.objects.filter(is_recommended=True)[:8],
            recent_products=recent_products,
            latest_news=NewsArticle.objects.filter(is_published=True)[:3],
            latest_promotions=Promotion.objects.filter(is_published=True)[:3],
            categories=Category.objects.all()[:6],
        )
        return context


class CatalogView(ListView):
    template_name = 'store/catalog.html'
    model = Product
    paginate_by = 12
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.select_related('category').all()
        query = self.request.GET.get('q', '').strip()
        category_slug = self.request.GET.get('category', '').strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(short_description__icontains=query)
                | Q(description__icontains=query)
            )
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['query'] = self.request.GET.get('q', '')
        return context


class ProductDetailView(DetailView):
    template_name = 'store/product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        recent = self.request.session.get('recently_viewed', [])
        if product.id in recent:
            recent.remove(product.id)
        recent.insert(0, product.id)
        self.request.session['recently_viewed'] = recent[:12]
        self.request.session.modified = True
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_products'] = Product.objects.filter(category=self.object.category).exclude(id=self.object.id)[:4]
        return context


class InfoPageView(DetailView):
    template_name = 'store/info_page.html'
    model = InfoPage
    slug_field = 'page_type'
    slug_url_kwarg = 'page_type'
    context_object_name = 'page'


class NewsListView(ListView):
    template_name = 'store/news_list.html'
    context_object_name = 'articles'
    model = NewsArticle

    def get_queryset(self):
        return NewsArticle.objects.filter(is_published=True)


class PromotionListView(ListView):
    template_name = 'store/promotions_list.html'
    context_object_name = 'promotions'
    model = Promotion

    def get_queryset(self):
        return Promotion.objects.filter(is_published=True)


def cart_view(request: HttpRequest) -> HttpResponse:
    cart = request.session.get('cart', {})
    product_ids = [int(pk) for pk in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    items = []
    total = Decimal('0.00')
    for product in products:
        quantity = cart[str(product.id)]['quantity']
        subtotal = product.price * quantity
        total += subtotal
        items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'store/cart.html', {'items': items, 'total': total})


def add_to_cart(request: HttpRequest, product_id: int) -> HttpResponse:
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.setdefault('cart', {})
    entry = cart.setdefault(str(product.id), {'quantity': 0})
    entry['quantity'] += 1
    request.session.modified = True
    messages.success(request, f'«{product.name}» добавлен в корзину.')
    return redirect(request.POST.get('next') or product.get_absolute_url())


def update_cart(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = max(0, int(request.POST.get('quantity', 0)))
        if quantity == 0:
            cart.pop(str(product_id), None)
        else:
            cart.setdefault(str(product_id), {'quantity': 0})['quantity'] = quantity
        request.session.modified = True
    return redirect('store:cart')


def remove_from_cart(request: HttpRequest, product_id: int) -> HttpResponse:
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect('store:cart')
