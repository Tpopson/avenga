from .models import Category


def catedropdown(request):
    categories = Category.objects.all()

    context ={
        'categories':categories
    }

    return context