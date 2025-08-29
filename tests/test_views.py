from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Profile
from advertisements.models import Advertisement, Application
from categories.models import Category
from ratings.models import Rating

User = get_user_model()


class CoreAccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.ad = Advertisement.objects.create(user=self.user, title="Test Ad", is_active=True)
        self.application = Application.objects.create(
            user=self.user, advertisement=self.ad, status="accepted"
        )

    def test_register_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
        }
        response = self.client.post(reverse("accounts:registration"), data)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        new_profile = Profile.objects.get(user__username="newuser")
        self.assertRedirects(response, reverse("accounts:profile", kwargs={"pk": new_profile.pk}))

    def test_login_logout(self):
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "password123"})
        self.assertEqual(response.status_code, 302)
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("accounts:logout_confirm"))
        self.assertRedirects(response, reverse("login"))

    def test_profile_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("accounts:profile", kwargs={"pk": self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.profile)


class AdvertisementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(name="TestCategory")  # обов'язкова категорія
        self.ad = Advertisement.objects.create(
            user=self.user,
            title="Test Ad",
            description="Test",
            is_active=True,
            location="Kyiv"
        )

    def test_create_advertisement(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("advertisements:create-advertisement")
        data = {
            "title": "New Ad",
            "description": "Test desc",
            "is_active": True,
            "location": "Kyiv",
            "price": 100,
            "categories": [self.category.id]
        }
        response = self.client.post(url, data)
        if response.status_code != 302:
            print(response.context["form"].errors)

        self.assertTrue(Advertisement.objects.filter(title="New Ad").exists())
        new_ad = Advertisement.objects.get(title="New Ad")
        self.assertEqual(new_ad.user, self.user)
        self.assertRedirects(response, reverse("accounts:profile", kwargs={"pk": self.user.profile.pk}))

class RatingsTests(TestCase):
    def setUp(self):
        self.client = Client()
        # створюємо користувача, який буде оцінювати
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.profile1, _ = Profile.objects.get_or_create(user=self.user1)

        # створюємо користувача, який буде оцінений
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.profile2, _ = Profile.objects.get_or_create(user=self.user2)

        # існуючий рейтинг
        self.rating = Rating.objects.create(
            profile=self.profile2,
            from_user=self.user1,
            rating=4,
            comment="Good work"
        )


    def test_user_info_view(self):
        self.client.login(username="user1", password="password123")
        url = reverse("ratings:user-info", kwargs={"user_id": self.user2.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("ratings", response.context)
        self.assertEqual(list(response.context["ratings"]), [self.rating])
        self.assertEqual(response.context["user_obj"], self.user2)
        self.assertIn("avg_rating", response.context)
        self.assertEqual(response.context["avg_rating"], 4)

    def test_make_feedback_create_new(self):
        self.client.login(username="user1", password="password123")
        url = reverse("ratings:feedback", kwargs={"user_id": self.user2.id})
        data = {"rating": 5, "comment": "Excellent!"}

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse("ratings:user-info", kwargs={"user_id": self.user2.id}))
        rating = Rating.objects.get(profile=self.profile2, from_user=self.user1)
        self.assertEqual(rating.rating, 5)
        self.assertEqual(rating.comment, "Excellent!")
