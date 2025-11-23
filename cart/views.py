from django.shortcuts import render,redirect
from store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()         
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    # Collect product variations from POST
    product_variation = []
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # =============== IF USER LOGGED IN ===================
    if request.user.is_authenticated:
        user = request.user
        cart_item_qs = CartItem.objects.filter(product=product, user=user)

    # =============== IF USER NOT LOGGED IN ===================
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart_item_qs = CartItem.objects.filter(product=product, cart=cart)

    # =========== CHECK FOR EXISTING VARIATIONS =============
    existing_variations_list = []  
    id_list = []

    for item in cart_item_qs:
        existing_variations = list(item.variations.all())
        existing_variations_list.append(sorted([v.id for v in existing_variations]))
        id_list.append(item.id)

    new_variations = sorted([v.id for v in product_variation])

    # If exact variation already exists → increase quantity
    if new_variations in existing_variations_list:
        index = existing_variations_list.index(new_variations)
        item = CartItem.objects.get(id=id_list[index])
        item.quantity += 1
        item.save()
    
    # Otherwise → create a new cart item
    else:
        item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=request.user if request.user.is_authenticated else None,
            cart=None if request.user.is_authenticated else cart
        )
        if product_variation:
            item.variations.set(product_variation)
        item.save()

    return redirect('cart')
    
def remove_cart(request, product_id,cart_item_id):
    
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
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
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(product=product, user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.filter(product=product, cart=cart,id=cart_item_id)
        
    cart_item.delete()
    return redirect('cart') 

def cart(request,total = 0, quantity = 0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
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

@login_required(login_url='login')
def checkout(request,total = 0, quantity = 0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
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
    return render(request,'cart/checkout.html',context)