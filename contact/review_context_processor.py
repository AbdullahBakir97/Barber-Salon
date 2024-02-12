from .models import Review

def get_review_data(request):
    data = Review.objects.all()
    return {'review_data': data}