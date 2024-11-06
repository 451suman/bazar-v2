from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
# Create your models here.
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE)
    full_name = models.CharField(max_length=50)
    address = models.CharField(max_length=60, null = True, blank = True)
    mobile = models.PositiveBigIntegerField() #

    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    def __str__(self):
        return self.title
    
class Product (models.Model):
    title = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='title', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=50, null = True, blank = True)
    return_policy = models.CharField(max_length=50, null = True, blank = True)

    def __str__(self):
        return self.title
    
class Cart (models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank= True)
    total = models.PositiveBigIntegerField(default=0)
    created_a = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart:" +str(self.id)
    
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()


    def __str__(self):
        return "Cart:" +str(self.cart.id) + "CartProduct: " +str(self.id)
    

ORDER_STATUS =(
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank= True)
    ordered_by = models.CharField(max_length=50) #
    shipping_address = models.CharField(max_length=60) #
    mobile = models.CharField(max_length=10) #
    email = models.EmailField(null = True, blank= True) #
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices= ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Order: " +str(self.id)


class Review(models.Model): 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    rating = models.PositiveIntegerField(default=1) 
    # Assuming a rating scale of 1-5 
    review_text = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"Review by {self.customer.full_name} for {self.product.title}"

class Contact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact by {self.customer.full_name}"