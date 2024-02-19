from .models import Review

def get_review_data(request):
    review_data = Review.objects.all()
    return {'review_data': review_data}
