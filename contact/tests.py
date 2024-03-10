from django.test import TestCase, Client
from django.urls import reverse
from contact.forms import ReviewCreateForm
from contact.models import Review

class ReviewFormTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_form_submission(self):
        # Define valid form data
        form_data = {
            'image': 'media/review_images/Category1.png',
            'barber': 1,  # Replace with valid barber ID
            'customer_name': 'John Doe',
            'email': 'john@example.com',
            'comment': 'Great service!',
            'rating': 5,
        }

        # Submit the form
        response = self.client.post(reverse('contact:visitor_review_create'), form_data)

        # Verify that the form submission was successful
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_submission_missing_required_fields(self):
        # Define invalid form data with missing required fields
        form_data = {
            'barber': 1,  # Provide a valid barber ID
            'customer_name': 'John Doe',
            'email': 'john@example.com',
            'comment': 'Great service!',
            'rating': 5,
        }

        # Submit the form
        response = self.client.post(reverse('contact:visitor_review_create'), form_data)

        # Verify that the form submission failed due to missing required fields
        self.assertEqual(response.status_code, 400)


    def test_invalid_form_submission_invalid_image(self):
        # Define invalid form data with an invalid image file
        form_data = {
            'image': 'invalid_image.jpg',  # Invalid image file path
            'barber': 1,
            'customer_name': 'John Doe',
            'email': 'john@example.com',
            'comment': 'Great service!',
            'rating': 5,
        }

        # Submit the form
        response = self.client.post(reverse('contact:visitor_review_create'), form_data)

        # Verify that the form submission failed due to an invalid image
        self.assertEqual(response.status_code, 400)

    def test_invalid_form_submission_invalid_rating(self):
        # Define invalid form data with an invalid rating value
        form_data = {
            'image': 'path/to/image.jpg',
            'barber': 1,
            'customer_name': 'John Doe',
            'email': 'john@example.com',
            'comment': 'Great service!',
            'rating': 6,  # Invalid rating value
        }

        # Submit the form
        response = self.client.post(reverse('contact:visitor_review_create'), form_data)

        # Verify that the form submission failed due to an invalid rating value
        self.assertEqual(response.status_code, 400)
