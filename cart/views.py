from django.shortcuts import render,redirect
from store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()         
    return cart

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id) #get the product
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    is_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        ex_var_list = []
        id_list = []

        for item in cart_item:
            existing_variation = list(item.variation.all())
            ex_var_list.append(set(v.id for v in existing_variation))  # store as a set of IDs
            id_list.append(item.id)

        product_variation_set = set(v.id for v in product_variation)

        if product_variation_set in ex_var_list:
            index = ex_var_list.index(product_variation_set)
            item_id = id_list[index]
            item = CartItem.objects.get(id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if product_variation:
                item.variation.set(product_variation)
            item.save()

    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if product_variation:
            cart_item.variation.set(product_variation)
        cart_item.save()
    return redirect('cart')
    
def remove_cart(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart') 

def remove_cart_item(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.filter(product=product, cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart') 

def cart(request,total = 0, quantity = 0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'tax': tax,
    }
    return render(request, 'cart/cart.html', context)


# def cart(request):
#     return render(request, 'cart/cart.html')    