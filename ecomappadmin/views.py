from urllib import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ecomapp.models import Admin, Order
from ecomappadmin.forms import AdminLoginForm


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

    #  ("Order Received", "Order Received"),
    # ("Order Processing", "Order Processing"),
    # ("On the way", "On the way"),
    # ("Order Completed", "Order Completed"),
    # ("Order Canceled", "Order Canceled"),
