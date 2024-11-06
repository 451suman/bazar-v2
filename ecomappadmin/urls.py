
from django.urls import include, path
from .views import *
app_name = "ecomappadmin"
urlpatterns = [
    path("admin-home/", AdminHomeView.as_view(), name="admin-home"),
    path("admin-login/", AdminLoginView.as_view(), name="admin-login"),
    path("admin-logout/", AdminLogouturl.as_view(), name="admin-logout"),
    path("admin-orders-received/", AdminOrderReceivedView.as_view(), name="admin-orders-received"),
    path("admin-orders-processing/", AdminOrderProcessingView.as_view(), name="admin-orders-processing"),
    path("admin-orders-completed/", AdminOrderCompletedView.as_view(), name="admin-orders-completed"),
    path("admin-orders-way/", AdminOrderWayView.as_view(), name="admin-orders-way"),
    path("admin-orders-canceled/", AdminOrderCanceledView.as_view(), name="admin-orders-canceled"),

    path("admin-order-detail/<int:pk>/", AdminOrderDetailView.as_view(), name="admin-order-detail"),
    
    path("admin-order-change-status-<int:pk>", AdminOrderStatusChangeView.as_view(), name="admin-order-change-status"),

    path("admin-add-product/", ProductAddView.as_view(), name="add-product"),
    path("product-list", ProductListView.as_view(), name="product-list"),
    path("product-detail/<slug:slug>/", ProductDetailView.as_view(), name="admin-product-detail"),
    path("product-edit/<slug:slug>/", ProductEditView.as_view(), name="admin-product-edit"),
    
    path("product-delete/<int:pk>/", ProductDeleteView.as_view(), name="admin-product-delete"),

    path("admin-add-category/", ADDCategoryView.as_view(), name="admin-add-category"),
    path("admin-category-list/", CategoryListView.as_view(), name="admin-category-list"),
    path("admin-update-category/<int:pk>/", CategoryUpdateView.as_view(), name="admin-update-category"),
    path('admin-delete-category/<int:pk>/', CategoryDeleteView.as_view(), name='admin-delete-category'),
    
    path("admin-contact-unread/", ShowUnreadContacts.as_view(), name="admin-contact-unread"),
    path("admin-contact-read/", ShowreadContacts.as_view(), name="admin-contact-read"),
    path("admin-contact-detail-<int:pk>/", ContactDetailView.as_view(), name="admin-contact-detail"),
    path("admin-mark-as-read-<int:pk>/", ContactMarkAsRead.as_view(), name="admin-mark-as-read"),

]

