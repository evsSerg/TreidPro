from .models import MenuItem


def menu_items(request):
    return {'site_menu_items': MenuItem.objects.filter(is_active=True)}


def cart_summary(request):
    cart = request.session.get('cart', {})
    total_items = sum(item.get('quantity', 0) for item in cart.values())
    return {'cart_items_count': total_items}
