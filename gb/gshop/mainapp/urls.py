from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('contact/', mainapp.contact, name='contact'),
    path('products/', mainapp.products, name='products'),

    path('category/<int:pk>/', mainapp.category, name='category'),
    path('product/<int:pk>/price/', mainapp.get_product_price),
    path('product/<int:pk>/', mainapp.product_page, name='product_page'),

]
