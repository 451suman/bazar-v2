from urllib import request
from django.shortcuts import redirect, render
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from ecomapp.forms import CheckoutForm, CustomerLoginForm, CustomerRegistrationsForm
from ecomapp.models import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import Avg
from django.shortcuts import get_object_or_404
# Create your views here.


# -------------------Customer Login register--------------------------------------------------------------
class CustomerRegisterView(CreateView):
    template_name = "customer/registration/signup.html"
    form_class = CustomerRegistrationsForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")

        # Create user with hashed password
        user = User.objects.create_user(
            username=username, password=password, email=email
        )

        form.instance.user = user
        login(self.request, user)

        messages.success(self.request, "Registration successful")

        return super().form_valid(form)


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:home")


class CustomerLoginView(FormView):
    template_name = "customer/registration/login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:home")

    # form_valid method is a type of post method and is available in createview formview and updateview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(
                self.request,
                self.template_name,
                {"form": self.form_class, "error": "Invalid credentials"},
            )

        return super().form_valid(form)


# -----------------------------------------------------------------------------------------------------------------------
#  The dispatch method is overridden. This method is called when a request is made to a view.
# It processes the request before any specific view logic is executed.
# just like static in java


class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
    
class customerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("ecomapp:customerlogin")

        return super().dispatch(request, *args, **kwargs)


class HomeView(EcomMixin, ListView):
    model = Product
    template_name = "customer/home/home.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["sliders"] = Product.objects.all().order_by("-id")[:3]

        context["products"] = Product.objects.all().order_by("-id")[:8]

        return context




# class ProductListView(EcomMixin, ListView):
#     model = Product
#     template_name = "customer/product_list/product_list.html"
#     context_object_name = "products"
#     paginate_by = 9

#     def get_queryset(self):
#         query = super().get_queryset()
#         query = Product.objects.all().order_by("-id")
        # return query

class ProductListView(EcomMixin, ListView):
    model = Product
    template_name = "customer/product_list/product_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        # Get the default queryset
        query = super().get_queryset()
        
        # Add the average rating to each product
        query = query.annotate(average_rating=Avg('review__rating')).order_by("-id")
        
        for product in query:
            if product.average_rating is not None:
                product.average_rating = round(product.average_rating) 
            
        return query  # Return the updated queryset



class CategoriesListView(EcomMixin, ListView):
    model = Product
    template_name = "customer/product_list/product_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            category__id=self.kwargs["cid"],
        ).order_by("-id")
        return query
    
class CategoryListView(EcomMixin, ListView):
    model = Category
    template_name = "customer/categoryNameList/categoryList.html"
    context_object_name="categorylist"

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Category"
        return context




class SearchView(EcomMixin, TemplateView):
    template_name = "customer/product_list/product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(
            Q(title__icontains=kw) | Q(description__icontains=kw) )
        print(results)
        context["products"] = results
        return context

# class idProductDetailView(EcomMixin, DetailView):
#     model = Product
#     template_name = "customer/productDetailPage/product_detail_page.html"
#     context_object_name = "product"


# class ProductDetailView(EcomMixin, TemplateView):
#     template_name = "customer/productDetailPage/product_detail_page.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         slug = self.kwargs["slug"]
#         print(slug)
#         context["product"] = Product.objects.get(slug=slug)
#         return context



class ProductDetailView(EcomMixin, TemplateView):
    template_name = "customer/productDetailPage/product_detail_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]

        # Get the product or return a 404 if not found
        product = get_object_or_404(Product, slug=slug)
        context["product"] = product
        context["reviewcount"] = Review.objects.filter(product=product).count()
        reviews = Review.objects.filter(product=product)
        context["all_review"] = reviews
        # Calculate the average rating
        average_rating_data = reviews.aggregate(Avg('rating'))['rating__avg']
        
        if average_rating_data is not None:
            average_rating = round(average_rating_data)
            if 1 <= average_rating <= 5:
                context["average_rating"] = average_rating
            else:
                context["average_rating"] = 0
        else:
            context["average_rating"] = 0
        
        can_review = False
        # Check if the user is authenticated and is a customer
        if self.request.user.is_authenticated and Customer.objects.filter(user=self.request.user).exists():
            order_items = Order.objects.filter(
                customer__user=self.request.user,
                cart__cartproduct__product=product,
                order_status="Order Completed"
            )

            has_reviewed = Review.objects.filter(customer__user=self.request.user, product=product).exists()

            if order_items.exists() and not has_reviewed:
                can_review = True

        context["can_review"] = can_review

        return context


        # print("-------------------------------------------------------------------")
        # print("-------------------------------------------------------------------")
        # print("-------------------------------------------------------------------")
        # print(can_review)
        # print(average_rating)

        context["can_review"] = can_review

        return context

class ReviewSubmit(View):
    def post(self, request, slug):
        rating = request.POST.get("rating")
        review_text = request.POST.get("review_text")
        product = get_object_or_404(Product, slug=slug)

        # Get or create the Customer instance based on the logged-in User
        customer= Customer.objects.get(user=request.user)

        # Create the review
        Review.objects.create(
            product=product,
            rating=rating,
            review_text=review_text,
            customer=customer  # Assign the Customer instance
        )

        # Redirect to product detail page
        return redirect('ecomapp:productdetail', slug=slug)

        


class AddToCartView(EcomMixin, View):
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


class MyCartView(EcomMixin, TemplateView):
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


class ManageCartView(EcomMixin, View):
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


class EmpytCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            # select all cart product and delete using cart id
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("ecomapp:mycart")


class CheckoutView(customerRequiredMixin, CreateView):
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

            # Check if an order already exists for this cart
            existing_order = Order.objects.filter(cart=cart_obj).first()
            if existing_order:
                messages.warning(self.request, "An order has already been placed for this cart.")
                return redirect(self.success_url)
            form.instance.customer = self.request.user.customer 
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"

            # Clear cart_id from session
            del self.request.session["cart_id"]

            messages.success(self.request, "Order has been received")
        else:
            return redirect("ecomapp:home")

        return super().form_valid(form)



class CustomerProfileView(customerRequiredMixin,TemplateView):
    template_name = "customer/my_account/myaccount.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer = self.request.user.customer
        context["customer"] = customer

        order = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = order
        return context


class CustomerOrderDetailView(customerRequiredMixin, DetailView):
    model = Order
    template_name = "customer/orderdetailView/customerorderdetail.html"
    context_object_name = "ord_obj"

from django.core.validators import EmailValidator
import re
class CustomerDetailChange(customerRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')

        if not full_name.isalpha():
            messages.error(request, "Full name must only contain letters.")
            return redirect('ecomapp:customerprofile')

        if not re.match(r'^[0-9]{10}$', mobile):
            messages.error(request, "Mobile number should be exactly 10 digits.")
            return redirect('ecomapp:customerprofile')

        try:
            EmailValidator()(email)  # Validate email format
        except Exception :
            messages.error(request, "Invalid email format.")
            return redirect('ecomapp:customerprofile')

        # All validations passed
        customer = request.user.customer
        customer.full_name = full_name
        customer.address = address  # Consider a more robust validation if needed
        customer.mobile = mobile
        customer.save()

        user = request.user
        user.email = email
        user.save()
        messages.success(request, "Your account details have been updated successfully.")

        return redirect('ecomapp:customerprofile')
