import os , django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

import random
from faker import Faker
from contact.models import Owner, Barber, Review, Category, Service, GalleryItem, Appointment, Message
from settings.models import Salon
from django.core.files import File






def generate_owners(n):
    fake = Faker()
    logo = ('01.jpg')
    for _ in range(n):
        owner = Owner.objects.create(
            name=fake.name(),
            logo=f"owner_logos/{random.randint(0,1)}",
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            website=fake.url(),
            work_days=fake.time(),
            about=fake.text(max_nb_chars=30),
        )
        
        # Create Salon after Owner creation
        Salon.objects.create(owner=owner)
        
        print(f'Salon created successfully for Owner: {owner.name}')
    print(f'{n} Owners were created successfully')


def generate_barbers(n):
    fake = Faker()
    image = ('01.jpg','02.jpg')
    for _ in range(n):
        barber = Barber.objects.create(
            name=fake.name(),
            image=f"barber_images/{random.randint(0,2)}",
            expertise=fake.text(max_nb_chars=30),
            experience_years=random.randint(1, 20),
        )

    print(f'{n} Barbers were created successfully')


def generate_reviews(n):
    fake = Faker()
    barbers = Barber.objects.all()
    image = ('01.jpg','02.jpg')
    for _ in range(n):
        Review.objects.create(
            image=f"review_images/{random.randint(0,2)}",
            barber=random.choice(barbers),
            customer_name=fake.name(),
            comment=fake.text(max_nb_chars=10),
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
    image = ('01.jpg','02.jpg')
    for _ in range(n):
        GalleryItem.objects.create(
            name=fake.word(),
            image=f"gallery_images/{random.randint(0,2)}",
            description=fake.text(max_nb_chars=15),
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
            message=fake.text(max_nb_chars=15),
        )
    print(f'{n} Appointments were created successfully')


def generate_messages(n):
    fake = Faker()
    for _ in range(n):
        Message.objects.create(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            message=fake.text(max_nb_chars=15),
        )
    print(f'{n} Messages were created successfully')


# generate_owners(1)
generate_barbers(4)
generate_reviews(4)
generate_categories(4)
generate_services(4)
generate_gallery_items(4)
generate_appointments(4)
generate_messages(4)
