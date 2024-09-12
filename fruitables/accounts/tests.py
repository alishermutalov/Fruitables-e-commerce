from django.contrib.auth.models import User
from django.test import TestCase
from .models import Profile

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            address='123 Test Street',
            phone='123456789',
            date_of_birth='1990-01-01'
        )

    def test_profile_creation(self):
        # Check that the profile was created correctly
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.address, '123 Test Street')
        self.assertEqual(self.profile.phone, '123456789')
        self.assertEqual(str(self.profile.date_of_birth), '1990-01-01')

    def test_profile_str(self):
        # Test the string representation of the profile
        self.assertEqual(str(self.profile), 'Profile of testuser')

    def test_profile_user_relationship(self):
        # Ensure the user and profile relationship is correct
        self.assertEqual(self.profile.user.username, self.user.username)
        self.assertEqual(self.profile.user, self.user)
