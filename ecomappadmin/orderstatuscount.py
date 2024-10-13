from ecomapp.models import Customer, Order
from django.db.models import Sum
def orderstatuscountFunc(request):
    Received = Order.objects.filter(order_status="Order Received").count()
    Processing = Order.objects.filter(order_status="Order Processing").count()
    way = Order.objects.filter(order_status="On the way").count()
    Completed = Order.objects.filter(order_status="Order Completed").count()
    Canceled = Order.objects.filter(order_status="Order Canceled").count()
    CustomerCount =Customer.objects.count()
    totalincome = Order.objects.aggregate(total=Sum('total'))['total'] or 0    
    return {
        "Received": Received,
        "Processing": Processing,
        "way": way,
        "Completed": Completed,
        "Canceled": Canceled,
        "CustomerCount": CustomerCount,
        "totalincome":totalincome,
    }

