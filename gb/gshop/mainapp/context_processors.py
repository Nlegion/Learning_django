from mainapp.models import ProductCategory

def pcategory(request):
    return {
        'pcategory': ProductCategory.objects.all()
    }