from django.db import models

from core.models.customer import Customer
from core.models.meal import Meal


class Order(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Delivered', 'Delivered')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    #all meals should be for the same Chef??
    ordered_date = models.DateField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
    delivery_date = models.DateField()

    def __str__(self):
        return self.id
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)


    def create_order_item(order, meal, quantity, total):
        order_item = OrderItem()
        order_item.order = order
        order_item.meal = meal
        order_item.quantity = quantity
        order_item.total = total
        order_item.save()
        return order_item