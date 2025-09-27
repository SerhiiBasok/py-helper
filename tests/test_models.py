from django.test import TestCase
from accounts.models import User, Profile
from advertisements.models import Application, Advertisement
from categories.models import Category
from ratings.models import Rating


class UserModelTest(TestCase):
    def test_str_returns_full_name_or_username(self):
        user1 = User.objects.create(username="user1", first_name="Walter", last_name="White")
        self.assertEqual(str(user1), "Walter White")
        user2 = User.objects.create(username="user2")
        self.assertEqual(str(user2), "user2")


class ProfileModelTest(TestCase):
    def test_str_returns_username_profile(self):
        user = User.objects.create(username="user3")
        profile, _ = Profile.objects.get_or_create(user=user)
        self.assertEqual(str(profile), "user3`s profile")

    def test_profile_categories_dont_break_str(self):
        user = User.objects.create(username="user4")
        profile, _ = Profile.objects.get_or_create(user=user)
        cat1 = Category.objects.create(name="Cooking")
        cat2 = Category.objects.create(name="Repairs")
        profile.categories.add(cat1, cat2)
        self.assertEqual(str(profile), "user4`s profile")



class AdvertisementApplicationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.category = Category.objects.create(name="Repairs")
        self.ad = Advertisement.objects.create(
            user=self.user1,
            title="Fix Water Heater",
            price=100,
            location="Vinnytsia",
            description="Need to fix broken water heater"
        )
        self.ad.categories.add(self.category)
        self.application = Application.objects.create(
            user=self.user2,
            advertisement=self.ad,
            message="I can help"
        )

    def test_accept_application_sets_status_and_deactivates_ad(self):
        self.application.accept()
        self.application.refresh_from_db()
        self.ad.refresh_from_db()

        self.assertEqual(self.application.status, "accepted")
        self.assertFalse(self.ad.is_active)

    def test_reject_application_sets_status(self):
        self.application.reject()
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, "rejected")

    def test_applicants_returns_user_ids(self):
        applicants = list(self.ad.applicants())
        self.assertIn(self.user2.id, applicants)


class CategoryModelTest(TestCase):
    def test_str_returns_name(self):
        category = Category.objects.create(name="Repairs")
        self.assertEqual(str(category), "Repairs")


class RatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="serhii", password="pass123")
        self.profile = self.user.profile
        self.rater = User.objects.create_user(username="alex", password="pass123")

    def test_str_with_user(self):
        rating = Rating.objects.create(
            profile=self.profile,
            from_user=self.rater,
            rating=5,
            comment="Great!"
        )
        expected_str = f"Rating 5 by alex for serhii"
        self.assertEqual(str(rating), expected_str)

    def test_str_anonymous_user(self):
        rating = Rating.objects.create(
            profile=self.profile,
            from_user=None,
            rating=4,
            comment="Good!"
        )
        expected_str = f"Rating 4 by Anonymous for serhii"
        self.assertEqual(str(rating), expected_str)