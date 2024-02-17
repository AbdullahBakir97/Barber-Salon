import os
import django
import random
from faker import Faker
from contact.models import Owner, Barber, Review, Category, Service, GalleryItem, Appointment, Message
from settings.models import Salon
from django.core.files import File
from django.core.files.images import ImageFile
from django.core.validators import MinValueValidator, MaxValueValidator


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


def generate_owners(n):
    fake = Faker()
    logo = ('01.jpg')
    for _ in range(n):
        owner = Owner.objects.create(
            name=fake.name(),
            logo=f"owner_logos/{[random.randint(0,1)]}"
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            website=fake.url(),
            work_days=fake.text(max_nb_chars=255),
            about=fake.text(),
        )
        
        # Create Salon after Owner creation
        Salon.objects.create(owner=owner)
        
        print(f'Salon created successfully for Owner: {owner.name}')
    print(f'{n} Owners were created successfully')


def generate_barbers(n):
    fake = Faker()
    for _ in range(n):
        barber = Barber.objects.create(
            name=fake.name(),
            expertise=fake.text(max_nb_chars=255),
            experience_years=random.randint(1, 20),
        )
        # Generate a dummy image for barber
        image_path = fake.image_path(category='people', width=400, height=400)
        barber.image.save(os.path.basename(image_path), File(open(image_path, 'rb')))
    print(f'{n} Barbers were created successfully')


def generate_reviews(n):
    fake = Faker()
    barbers = Barber.objects.all()
    for _ in range(n):
        Review.objects.create(
            image=ImageFile(open(fake.image_path(), 'rb')),
            barber=random.choice(barbers),
            customer_name=fake.name(),
            comment=fake.text(),
            rating=random.randint(1, 5),
        )
    print(f'{n} Reviews were created successfully')


def generate_categories(n):
    fake = Faker()
    for _ in range(n):
        Category.objects.create(
            name=fake.word(),
        )
    print(f'{n} Categories were created successfully')


def generate_services(n):
    fake = Faker()
    categories = Category.objects.all()
    for _ in range(n):
        Service.objects.create(
            name=fake.word(),
            category=random.choice(categories),
            price=random.uniform(10.0, 100.0),
        )
    print(f'{n} Services were created successfully')


def generate_gallery_items(n):
    fake = Faker()
    categories = Category.objects.all()
    services = Service.objects.all()
    for _ in range(n):
        GalleryItem.objects.create(
            name=fake.word(),
            image=ImageFile(open(fake.image_path(), 'rb')),
            description=fake.text(),
            category=random.choice(categories),
            service=random.choice(services),
        )
    print(f'{n} GalleryItems were created successfully')


def generate_appointments(n):
    fake = Faker()
    barbers = Barber.objects.all()
    services = Service.objects.all()
    for _ in range(n):
        Appointment.objects.create(
            name=fake.name(),
            barber=random.choice(barbers),
            date=fake.date_this_month(),
            time=fake.time(),
            service_type=random.choice(services),
            phone=fake.phone_number(),
            email=fake.email(),
            message=fake.text(),
        )
    print(f'{n} Appointments were created successfully')


def generate_messages(n):
    fake = Faker()
    for _ in range(n):
        Message.objects.create(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            message=fake.text(),
        )
    print(f'{n} Messages were created successfully')


generate_owners(1)
generate_barbers(5)
generate_reviews(10)
generate_categories(4)
generate_services(16)
generate_gallery_items(10)
generate_appointments(10)
generate_messages(5)
