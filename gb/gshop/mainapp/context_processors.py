from mainapp.models import ProductCategory

def pcategory(request):
    return {
        'pcategory': ProductCategory.objects.filter(is_active=True)
    }