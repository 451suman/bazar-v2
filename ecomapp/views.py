from django.shortcuts import redirect, render
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from ecomapp.forms import CheckoutForm, CustomerRegistrationsForm
from ecomapp.models import *
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.

class CustomerRegisterView(CreateView):
    template_name = 'customer/registration/signup.html'
    form_class = CustomerRegistrationsForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")

        # Create user with hashed password
        user = User.objects.create_user(username=username, password=password, email=email)

        form.instance.user = user
        login(self.request, user)
        
        messages.success(self.request, "Registration successful")

        return super().form_valid(form)


class HomeView(ListView):
    model = Product
    template_name = "customer/home/home.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["sliders"] = Product.objects.all().order_by("-id")[:3]

        context["products"] = Product.objects.all().order_by("-id")[:8]

        return context


class ProductListView(ListView):
    model = Product
    template_name = "customer/product_list/product_list.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        query = super().get_queryset()
        query = Product.objects.all().order_by("-id")
        return query


class ProductDetailView(DetailView):
    model = Product
    template_name = "customer/productDetailPage/product_detail_page.html"
    context_object_name = "product"


class AddToCartView(View):
    def get(self, request, **kwargs):
        # Get product id from requested url
        product_id = self.kwargs["pro_id"]

        # Get product
        product_obj = Product.objects.get(id=product_id)

        # Check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            # Check if the product is already in the cart
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

            # Items already in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

            # New item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj,
                    product=product_obj,
                    rate=product_obj.selling_price,
                    quantity=1,
                    subtotal=product_obj.selling_price,
                )
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)

            cartproduct = CartProduct.objects.create(
                cart=cart_obj,
                product=product_obj,
                rate=product_obj.selling_price,
                quantity=1,
                subtotal=product_obj.selling_price,
            )
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            request.session["cart_id"] = cart_obj.id  # Save cart_id in session

        # Redirect to the cart view
        return redirect("ecomapp:mycart")


class MyCartView(TemplateView):
    template_name = "customer/cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        # print(cart_id)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            # print(cart.__dict__)
        else:
            cart = None
        context["cart"] = cart
        return context


class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        print("this is manage cart section")
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            # delete cartproduct products
            cp_obj.delete()

        else:
            pass

        # print (cp_id, action)
        return redirect("ecomapp:mycart")


class EmpytCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            # select all cart product and delete using cart id
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("ecomapp:mycart")

class CheckoutView(CreateView):
    model = Order  # Define the model here
    template_name = "customer/checkout/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("ecomapp:home")



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None

        context["cart"] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)

            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"

            # now delete cart_id which is store in Session
            del self.request.session["cart_id"]

            messages.success(self.request, "Order has been received")
        else:
            return redirect("ecomapp:home")

        return super().form_valid(form)