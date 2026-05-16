from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserTests(TestCase):
    def test_create_user(self):
        """Teszteljük, hogy a felhasználó megfelelően jön-e létre."""
        user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Teszteljük az admin(superuser) létrehozását."""
        admin_user = User.objects.create_superuser(
            username='adminuser', 
            email='admin@example.com', 
            password='superuserpassword123'
        )
        self.assertEqual(admin_user.username, 'adminuser')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

