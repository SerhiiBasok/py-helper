from django.test import TestCase
from accounts.models import User, Profile
from accounts.forms import ProfileForm
from advertisements.forms import AdvertisementForm
from categories.models import Category
from ratings.forms import FeedbackForm


class ProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.profile = self.user.profile
        self.category1 = Category.objects.create(name="Test1")
        self.category2 = Category.objects.create(name="Test2")

    def test_phone_validation_allows_digits_only(self):
        form_data = {"phone": "1234567890"}
        form = ProfileForm(data=form_data, instance=self.profile, user=self.user)
        self.assertTrue(form.is_valid())

    def test_phone_validation_rejects_non_digits(self):
        form_data = {"phone": "abc123"}
        form = ProfileForm(data=form_data, instance=self.profile, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)

    def test_first_and_last_name_are_saved_to_user(self):
        form_data = {
            "first_name": "Walter",
            "last_name": "White",
            "phone": "12345",
            "categories": [],
        }
        form = ProfileForm(data=form_data, instance=self.profile, user=self.user)
        self.assertTrue(form.is_valid())
        profile = form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Walter")
        self.assertEqual(self.user.last_name, "White")
        self.assertEqual(profile.phone, "12345")

    def test_categories_are_set_correctly(self):
        form_data = {
            "first_name": "Walter",
            "last_name": "White",
            "phone": "12345",
            "categories": [self.category1.id, self.category2.id],
        }
        form = ProfileForm(data=form_data, instance=self.profile, user=self.user)
        self.assertTrue(form.is_valid())
        profile = form.save()
        self.assertEqual(
            list(profile.categories.all().order_by("id")),
            [self.category1, self.category2]
        )

    def test_categories_cleared_if_not_provided(self):
        self.profile.categories.set([self.category1, self.category2])
        form_data = {
            "first_name": "Walter",
            "last_name": "White",
            "phone": "12345",
            "categories": [],
        }
        form = ProfileForm(data=form_data, instance=self.profile, user=self.user)
        self.assertTrue(form.is_valid())
        profile = form.save()
        self.assertEqual(profile.categories.count(), 0)


class AdvertisementFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.category1 = Category.objects.create(name="Test1")
        self.category2 = Category.objects.create(name="Test2")

    def test_categories_field_accepts_multiple_categories(self):
        form_data = {
            "title": "Test Ad",
            "price": 100,
            "location": "Kyiv",
            "description": "Test description",
            "categories": [self.category1.id, self.category2.id],
        }
        form = AdvertisementForm(data=form_data)
        self.assertTrue(form.is_valid())
        ad = form.save(commit=False)
        ad.user = self.user
        ad.save()
        form.save_m2m()
        self.assertEqual(list(ad.categories.all().order_by("id")),
                         [self.category1, self.category2])

    def test_categories_field_can_be_empty(self):
        form_data = {
            "title": "Test Ad",
            "price": 50,
            "location": "Lviv",
            "description": "Another description",
            "categories": [],
        }
        form = AdvertisementForm(data=form_data)
        self.assertTrue(form.is_valid())
        ad = form.save(commit=False)
        ad.user = self.user
        ad.save()
        form.save_m2m()
        self.assertEqual(ad.categories.count(), 0)


class FeedbackFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.profile = self.user.profile

    def test_feedback_form_valid_data(self):
        form_data = {
            "rating": 5,
            "comment": "Great service!"
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())
        feedback = form.save(commit=False)
        feedback.profile = self.profile
        feedback.from_user = self.user
        feedback.save()
        self.assertEqual(feedback.rating, 5)
        self.assertEqual(feedback.comment, "Great service!")
        self.assertEqual(feedback.profile, self.profile)
        self.assertEqual(feedback.from_user, self.user)

    def test_feedback_form_empty_comment(self):
        form_data = {
            "rating": 3,
            "comment": ""
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())
        feedback = form.save(commit=False)
        feedback.profile = self.profile
        feedback.from_user = self.user
        feedback.save()
        self.assertEqual(feedback.rating, 3)
        self.assertEqual(feedback.comment, "")