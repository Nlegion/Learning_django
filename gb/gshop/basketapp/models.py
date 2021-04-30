from django.db import models
from mainapp.models import Product
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property


class Basket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)
    add_datetime = models.DateTimeField('время', auto_now_add=True)
    update_datetime = models.DateTimeField('время', auto_now=True)

    @cached_property
    def product_cost(self):
        return self.product.price * self.quantity

    # @classmethod
    # def get_item(cls,pk):
    #     return cls.objects.filter(pk=pk).first()

