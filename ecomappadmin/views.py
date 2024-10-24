from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ecomapp.models import ORDER_STATUS, Admin, Category, Customer, Order, Product
from ecomappadmin.forms import AddProductForm, AdminLoginForm, CategoryForm
from django.db.models import Sum


# Create your views here.
class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and (Admin.objects.filter(user=request.user).exists() or request.user.is_superuser)
        ):
            pass
        else:
            return redirect("ecomappadmin:admin-login")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "admin/home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newcustomer"] = Customer.objects.all().order_by("-id")[:7]
        context["totalProducts"] = Product.objects.all().count()
        context["totalCategory"] = Category.objects.all().count()
        context["totalorder"] = Order.objects.all().count()
        return context


from django.contrib.auth.models import User


class AdminLoginView(FormView):
    template_name = "admin/registration/adminlogin.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("ecomappadmin:admin-home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        print("------------------------------------------------------")
        print("------------------------------------------------------")
        print("------------------------------------------------------")
        print("------------------------------------------------------")
        print(f"Authenticated user: {usr}")  # Check if user is authenticated
        print(f"Is superuser: {usr.is_superuser if usr else 'User not found'}")  # Check superuser status
        if usr is not None:
            # Check if user is superuser or admin
            if usr.is_superuser or Admin.objects.filter(user=usr).exists():
                messages.success(self.request, "Welcome Admin!")
                login(self.request, usr)
                return super().form_valid(form)  # Redirect to success URL

        else:
            return render(
                self.request,
                self.template_name,
                {"form": self.form_class, "error": "Invalid credentials"},
            )


class AdminLogouturl(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:home")


# --------------------------orders ---------------------------------
class AdminOrderReceivedView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "admin/order_list/order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Received"
        context["allorders"] = Order.objects.filter(
            order_status="Order Received"
        ).order_by("-id")
        return context


class AdminOrderProcessingView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "admin/order_list/order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Processing"
        context["allorders"] = Order.objects.filter(
            order_status="Order Processing"
        ).order_by("-id")
        return context


class AdminOrderCompletedView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "admin/order_list/order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Completed"
        context["allorders"] = Order.objects.filter(
            order_status="Order Completed"
        ).order_by(
            "-id"
        )  # Corrected here
        return context


class AdminOrderWayView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "admin/order_list/order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Completed"
        context["allorders"] = Order.objects.filter(order_status="On the way").order_by(
            "-id"
        )
        return context


class AdminOrderCanceledView(AdminRequiredMixin, ListView):
    model = Order
    template_name = "admin/order_list/order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Canceled"
        context["allorders"] = Order.objects.filter(
            order_status="Order Canceled"
        ).order_by("-id")
        return context


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    model = Order
    template_name = "admin/order_detail/orderdetail.html"
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        # order status comes from model which is used in ordermodel
        return context


class AdminOrderStatusChangeView(AdminRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
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
        return redirect("ecomappadmin:admin-order-detail", pk=order_id)


class ProductAddView(AdminRequiredMixin, CreateView):
    model = Product
    template_name = "admin/product_category_crud/addproductcategory.html"
    form_class = AddProductForm
    # success_url = reverse_lazy("ecomappadmin:admin-product-detail", )

    def form_valid(self, form):
        messages.success(self.request, "Product added successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add New Product"
        return context

    def get_success_url(self):
        return reverse(
            "ecomappadmin:admin-product-detail", kwargs={"slug": self.object.slug}
        )


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


class ProductEditView(AdminRequiredMixin, UpdateView):
    model = Product
    template_name = "admin/product_category_crud/addproductcategory.html"
    form_class = AddProductForm

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Update Product Details"
        return context

    def form_valid(self, form):
        product = form.save()  # Save the form and get the product instance
        messages.success(self.request, "Product updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "ecomappadmin:admin-product-detail", kwargs={"slug": self.object.slug}
        )


class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy(
        "ecomappadmin:product-list"
    )  # Ensure this is the correct URL name


class ADDCategoryView(AdminRequiredMixin, CreateView):
    model = Category
    template_name = "admin/product_category_crud/addproductcategory.html"
    form_class = CategoryForm
    success_url = reverse_lazy(
        "ecomappadmin:admin-category-list"
    )  # Ensure this is the correct URL name

    def form_valid(self, form):
        messages.success(self.request, "Category added successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):  # Accept **kwargs to maintain context
        context = super().get_context_data(**kwargs)
        context["title"] = "Add New Category"
        return context


class CategoryListView(AdminRequiredMixin, ListView):
    model = Category
    template_name = "admin/category_list_page/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        query = super().get_queryset()
        query.order_by("-id")
        return query


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    template_name = "admin/product_category_crud/addproductcategory.html"
    form_class = CategoryForm
    success_url = reverse_lazy(
        "ecomappadmin:admin-category-list"
    )  # Ensure this is the correct URL name

    def form_valid(self, form):
        messages.success(self.request, "Category Updated successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):  # Accept **kwargs to maintain context
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Category"
        return context


class CategoryDeleteView(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cid = kwargs.get("pk")
        category = Category.objects.get(pk=cid)
        category.delete()
        messages.success(request, "Category deleted successfully")
        return redirect("ecomappadmin:admin-category-list")
