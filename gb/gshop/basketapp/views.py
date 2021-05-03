from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.db import connection
from django.db.models import F
from gshop.settings import LOGIN_URL
from basketapp.models import Basket


@login_required
def index(request):
    basket = request.user.basket.all()
    context = {
        'page_title': 'корзина',
        'basket': basket,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, product_pk):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse('main:product_page',
                    kwargs={'pk': product_pk}))

    basket_item, _ = Basket.objects.get_or_create(
        user=request.user,
        product_id=product_pk
    )
    # basket_item.quantity += 1
    basket_item.quantity = F('quantity') + 1
    basket_item.save()
    print(connection.queries)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, basket_pk):
    item = get_object_or_404(Basket, pk=basket_pk)
    item.delete()
    return HttpResponseRedirect(reverse('basket:index'))


def update(request, basket_pk, qty):
    if request.is_ajax():
        item = Basket.objects.filter(pk=basket_pk).first()
        if not item:
            return JsonResponse({'status': False})
        if qty == 0:
            item.delete()
        else:
            item.qty = qty
            item.save()
        basket_summary_html = render_to_string(
            'basketapp/includes/basket_summary.html',
            request=request
        )
        print(basket_summary_html)
        return JsonResponse({'status': True,
                             'basket_summary': basket_summary_html,
                             'qty': qty})
