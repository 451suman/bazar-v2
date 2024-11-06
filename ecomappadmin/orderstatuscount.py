from ecomapp.models import Contact, Customer, Order
from django.db.models import Sum
def orderstatuscountFunc(request):
    Received = Order.objects.filter(order_status="Order Received").count()
    Processing = Order.objects.filter(order_status="Order Processing").count()
    way = Order.objects.filter(order_status="On the way").count()
    Completed = Order.objects.filter(order_status="Order Completed").count()
    Canceled = Order.objects.filter(order_status="Order Canceled").count()
    CustomerCount =Customer.objects.count()
    totalincome = Order.objects.aggregate(total=Sum('total'))['total'] or 0    


    contacts_count_read = Contact.objects.filter(read = True).count()
    contacts_count_unread= Contact.objects.filter(read = False).count()


    return {
        "Received": Received,
        "Processing": Processing,
        "way": way,
        "Completed": Completed,
        "Canceled": Canceled,
        "CustomerCount": CustomerCount,
        "totalincome":totalincome,
        "contacts_count_read":contacts_count_read,
        "contacts_count_unread":contacts_count_unread,
    }

