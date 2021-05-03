import random

from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache
from django.db.models.signals import pre_save
from django.dispatch import receiver
from gshop import settings
from django.db import connection
from mainapp.models import Product, ProductCategory


def get_products():
    if settings.LOW_CACHE:
        key = 'all_products'
        products = cache.get(key)
        if products is None:
            products = Product.get_items()
            cache.set(key, products)
        return products
    return Product.get_items()


def get_products_by_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}_products'
        products = cache.get(key)
        if products is None:
            products = Product.get_items().filter(category_id=pk)
            cache.set(key, products)
        return products
    return Product.get_items().filter(category_id=pk)


def get_hot_product():
    product_ids = get_products().values_list('id', flat=True)
    random_id = random.choice(product_ids)
    return Product.objects.get(pk=random_id)


def same_products(hot_product):
    return Product.get_items().filter(category=hot_product.category). \
               exclude(pk=hot_product.pk)[:4]


def index(request):
    context = {'page_title': 'Главная', }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    contacts = [
        {'city': 'Москва',
         'phone': '+7-888-888-8888',
         'email': 'smth@google.com',
         'address': 'В пределах МКАД'},
        {'city': 'Москва 1',
         'phone': '+7-888-888-8888',
         'email': 'smth@google.com',
         'address': 'В пределах МКАД'},
        {'city': 'Москва 2',
         'phone': '+7-888-888-8888',
         'email': 'smth@google.com',
         'address': 'В пределах МКАД'},
    ]
    context = {'page_title': 'Контакты',
               'contacts': contacts,
               }
    return render(request, 'mainapp/contact.html', context)


@never_cache
def products(request):
    hot_product = get_hot_product()
    context = {
        'page_title': 'Каталог',
        'hot_product': hot_product,
        'same_product': same_products(hot_product),
    }
    return render(request, 'mainapp/products.html', context)


# @cache_page(3600)
def category(request, pk):
    page_num = request.GET.get('page', 1)
    if pk == 0:
        category = {'pk': 0, 'name': 'все'}
        products = get_products()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = get_products_by_category(pk)

    products_paginator = Paginator(products, 2)
    try:
        products = products_paginator.page(page_num)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)
    context = {
        'page_title': 'Каталог',
        'category': category,
        'products': products, }
    return render(request, 'mainapp/category_products.html', context)


def product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'page_title': 'страница продукта',
        'product': product,
    }
    return render(request, 'mainapp/product_page.html', context)


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=pk).first()
        return JsonResponse(
            {'price': product and product.price or 0}
        )


def db_profile_by_type(sender, q_type, queries):
    print(f'db profile {q_type} for {sender}:')
    for query in filter(lambda x: q_type in x,
                        map(lambda x: x['sql'],
                            queries)):
        print(query)


@receiver(pre_save, sender=ProductCategory)
def update_prod_cat_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
