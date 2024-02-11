from .models import Salon


def get_salon_data(request):
    data = Salon.objects.last()
    return {'salon_data':data}
