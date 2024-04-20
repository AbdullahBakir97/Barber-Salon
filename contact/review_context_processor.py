from .models import Review, Barber
from django.core.paginator import Paginator

def get_review_data(request):
    all_reviews = Review.objects.order_by('-id')
    barber_list = Barber.objects.all()
    # Pagination
    paginator = Paginator(all_reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return {
        'review_data': page_obj, 'barber_list':barber_list
    }
