from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date
from .models import Leave

User = get_user_model()

class LeaveModelTests(TestCase):
    def setUp(self):
        """Ez a metódus minden teszt előtt lefut. Felépíti a teszt-adatbázist."""
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123'
        )
        
        self.leave = Leave.objects.create(
            user=self.user,
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 5),
            leave_type='PTO',
            notes='Nyaralás'
        )

    def test_leave_creation(self):
        """Megvizsgáljuk, hogy az objektum tényleg létrejött-e és jók-e az adatai."""
        self.assertEqual(Leave.objects.count(), 1)
        self.assertEqual(self.leave.user.username, 'testuser')
        self.assertEqual(self.leave.leave_type, 'PTO')
        self.assertEqual(self.leave.notes, 'Nyaralás')

    def test_leave_str_representation(self):
        """A modell __str__ metódusának ellenőrzése."""
        expected_str = "testuser - Paid Time Off (2026-06-01 -> 2026-06-05)"
        self.assertEqual(str(self.leave), expected_str)

    def test_leave_date_validation(self):
        """Teszteljük, hogy a rendszer visszautasítja-e a hibás idősávokat."""
        invalid_leave = Leave(
            user=self.user,
            start_date=date(2026, 6, 10),
            end_date=date(2026, 6, 5), # A végdátum régebbi
            leave_type='PTO'
        )
        
        # A ValidationError-t várjuk, ha rosszak a dátumok
        with self.assertRaises(ValidationError):
            invalid_leave.save()


