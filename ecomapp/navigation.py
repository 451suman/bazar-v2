from .models import Category, Product

def navigationFunc(request):
    categories = Category.objects.all().order_by("-id")[:5]  # Fetch all categories for navgations
    deals = Product.objects.all().order_by("-id")
    return {
        "categories": categories,
        "deals": deals,
    }
