from ecomapp.models import Order

def orderstatuscountFunc(request):
    Received = Order.objects.filter(order_status="Order Received").count()
    Processing = Order.objects.filter(order_status="Order Processing").count()
    way = Order.objects.filter(order_status="On the way").count()
    Completed = Order.objects.filter(order_status="Order Completed").count()
    Canceled = Order.objects.filter(order_status="Order Canceled").count()

    return {
        "Received": Received,
        "Processing": Processing,
        "way": way,
        "Completed": Completed,
        "Canceled": Canceled,
    }
