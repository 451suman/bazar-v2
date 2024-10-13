from urllib import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ecomapp.models import ORDER_STATUS, Admin, Category, Customer, Order, Product
from ecomappadmin.forms import AddProductForm, AdminLoginForm
from django.db.models import Sum



# Create your views here.
class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and Admin.objects.filter(user=request.user).exists()
        ):
            pass
        else:
            return redirect("ecomappadmin:admin-login")
        return super().dispatch(request, *args, **kwargs)




class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "admin/home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["CustomerCount"] = Customer.objects.count()  # More efficient
        context["totalincome"] = Order.objects.aggregate(total=Sum('total'))['total'] or 0
        context["newcustomer"] = Customer.objects.all().order_by("-id") [:10]
        context["totalProducts"] = Product.objects.all().count()
        context["totalCategory"] = Category.objects.all().count()
        context["totalorder"]= Order.objects.all().count()
        return context






class AdminLoginView(FormView):
    template_name = "admin/registration/adminlogin.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("ecomappadmin:admin-home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            messages.success(self.request, f"Welcome Admin!")
            login(self.request, usr)
        else:
            return render(
                self.request,
                self.template_name,
                {"form": self.form_class, "error": "Invalid credentials"},
            )
        return super().form_valid(form)


# --------------------------orders ---------------------------------
class AdminOrderReceivedView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "admin/order_list/order_list.html"
    context_object_name = "allorders"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(order_status="Order Received").order_by("-id")
        return query


class AdminOrderProcessingView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "admin/order_list/order_list.html"
    context_object_name = "allorders"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(order_status="Order Processing").order_by("-id")
        return query


class AdminOrderCompletedView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "admin/order_list/order_list.html"
    context_object_name = "allorders"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(order_status="Order Completed").order_by("-id")
        return query


class AdminOrderWayView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "admin/order_list/order_list.html"
    context_object_name = "allorders"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(order_status="On the way").order_by("-id")
        return query


class AdminOrderCanceledView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "admin/order_list/order_list.html"
    context_object_name = "allorders"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(order_status="Order Canceled").order_by("-id")
        return query


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    model = Order
    template_name = "admin/order_detail/orderdetail.html"
    context_object_name="ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS  
        # order status comes from model which is used in ordermodel
        return context

class AdminOrderStatusChangeView(AdminRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        # print("------------------------------------------------------------------------------------------")
        # print("------------------------------------------------------------------------------------------")
        # print("------------------------------------------------------------------------------------------")
        # print("------------------------------------------------------------------------------------------")
        # print("------------------------------------------------------------------------------------------")
        # print(order_id)
        order_obj = Order.objects.get(pk=order_id)
        newstatus = request.POST.get("Staus")
        order_obj.order_status = newstatus
        order_obj.save()
        return redirect("ecomappadmin:admin-order-detail", pk = order_id)



class ProductAddView(AdminRequiredMixin, CreateView):
    model = Product
    template_name = "admin/product_crud/addproduct.html"
    form_class = AddProductForm
    success_url = reverse_lazy("ecomappadmin:add-product")

    def form_valid(self, form):
        messages.success(self.request, "Product added successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add New Product"
        return context


    
class ProductListView(AdminRequiredMixin, ListView):
    model = Product
    template_name = "admin/productlist/productlist.html"
    context_object_name = "products"
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        return query.order_by("-id")


class ProductDetailView(AdminRequiredMixin, DetailView):
    model = Product
    template_name = "admin/productdetailpage/productdetailpage.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Product"
        return context
