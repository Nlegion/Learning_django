import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from mainapp.models import Product, ProductCategory


#def get_menu():
 #   return ProductCategory.objects.all()


def get_hot_product():
    product_ids = Product.objects.values_list('id', flat=True).all()
    random_id = random.choice(product_ids)
    return Product.objects.get(pk=random_id)


def same_products(hot_product):
    return Product.objects.filter(category=hot_product.category). \
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


def products(request):
    hot_product = get_hot_product()
    context = {
        'page_title': 'Каталог',
        'hot_product': hot_product,
        'same_product': same_products(hot_product),
        #'pcategory': get_menu(),
    }
    return render(request, 'mainapp/products.html', context)


def category(request, pk):
    page_num = request.GET.get('page', 1)
    if pk == 0:
        category = {'pk': 0, 'name': 'все'}
        products = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.all()

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
        #'categories': get_menu(),
        'products': products, }
    return render(request, 'mainapp/category_products.html', context)


def product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'page_title': 'страница продукта',
        'product': product,
        #'categories': get_menu(),
    }
    return render(request, 'mainapp/product_page.html', context)
