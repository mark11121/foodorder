from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from accounts.views import customer_or_user_login_required
from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@customer_or_user_login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

@customer_or_user_login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@customer_or_user_login_required
def cart_detail(request):
    cart = Cart(request)
    # 使用 for in 的時候，他會開始迭代，並且呼叫 `__iter__`
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })
    return render(request, 'cart/detail.html', {'cart': cart})
