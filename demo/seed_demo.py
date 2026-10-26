"""Fill an empty, migrated database with clearly fictional demo data."""
import datetime, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
import django
django.setup()
from contact.models import Owner, Barber, Review, Category, Service, GalleryItem, Appointment, Message
from settings.models import Salon

random.seed(7)
owner = Owner.objects.create(
    name="Demo Barber Studio", email="hello@example.com", phone="+49 30 0000000",
    address="Musterstraße 1\n10115 Berlin", website="https://example.com",
    work_days="Montag-Samstag", logo="barbershop.png", about="Fictional salon used for the demo database.",
)
Salon.objects.create(owner=owner, web_icon="barbershop.png")

cats = {n: Category.objects.create(name=n) for n in ["Haarschnitt", "Bart", "Pflege"]}
services = [Service.objects.create(name=n, category=cats[c], price=p) for n, c, p in [
    ("Herrenhaarschnitt", "Haarschnitt", 25), ("Kinderhaarschnitt", "Haarschnitt", 18),
    ("Fade", "Haarschnitt", 28), ("Bart trimmen", "Bart", 15), ("Nassrasur", "Bart", 20),
    ("Haarschnitt + Bart", "Bart", 38), ("Gesichtsmaske", "Pflege", 15), ("Augenbrauen", "Pflege", 8),
]]
barbers = [Barber.objects.create(name=n, expertise=e, experience_years=y, image="barbershop.png") for n, e, y in [
    ("Demo Barber A", "Fades and classic cuts", 8), ("Demo Barber B", "Beard styling", 5),
    ("Demo Barber C", "Kids and family cuts", 3),
]]
for i, (r, c) in enumerate([(5, "Great cut, friendly team."), (4, "Quick and tidy beard trim."),
                            (5, "Booked online, no waiting."), (4, "Good value for the price.")], 1):
    Review.objects.create(customer_name=f"Demo Customer {i}", email=f"customer{i}@example.com",
                          comment=c, rating=r, barber=barbers[i % 3])
for s in services[:4]:
    GalleryItem.objects.create(name=s.name, image="barbershop.png", description=f"Example: {s.name}",
                               category=s.category, service=s)
start = datetime.date(2026, 1, 5)
for i in range(1, 13):
    Appointment.objects.create(name=f"Demo Customer {i}", barber=barbers[i % 3],
        date=start + datetime.timedelta(days=i), time=datetime.time(9 + i % 9, 0),
        service_type=services[i % len(services)], phone="+49 30 0000000",
        email=f"customer{i}@example.com", message="Demo booking")
for i in range(1, 4):
    Message.objects.create(name=f"Demo Visitor {i}", email=f"visitor{i}@example.com",
                           phone="+49 30 0000000", message="Demo contact message.")
print("demo data created")
