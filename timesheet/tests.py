from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import IntegrityError
from datetime import date
import json

from clients.models import Client
from projects.models import Project
from .models import TimeEntry
from .views import parse_hours, format_hours

User = get_user_model()

class TimesheetParserTests(TestCase):
    def test_parse_hours(self):
        """Teszteljük, hogy a beírt szövegeket jól konvertálja-e tizedes számra."""
        self.assertEqual(parse_hours("8"), 8.0)
        self.assertEqual(parse_hours("8ó"), 8.0)
        self.assertEqual(parse_hours("7ó 30p"), 7.5)
        self.assertEqual(parse_hours("7:45"), 7.75)
        self.assertEqual(parse_hours("45p"), 0.75)
        self.assertEqual(parse_hours("8.5"), 8.5)
        self.assertEqual(parse_hours("8,25"), 8.25)
        self.assertEqual(parse_hours(""), 0.0)
        self.assertEqual(parse_hours("alma"), 0.0)

    def test_format_hours(self):
        """Teszteljük a tizedes formátumból -> olvasható óra/perc formátumot."""
        self.assertEqual(format_hours(8.0), "8ó")
        self.assertEqual(format_hours(7.5), "7ó 30p")
        self.assertEqual(format_hours(7.75), "7ó 45p")
        self.assertEqual(format_hours(0.75), "45p")
        self.assertEqual(format_hours(0), "")

class TimesheetModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client_obj = Client.objects.create(name='Test Client')
        self.project = Project.objects.create(name='Test Project', client=self.client_obj)
        self.project.assigned_users.add(self.user)

    def test_create_time_entry(self):
        entry = TimeEntry.objects.create(
            user=self.user,
            project=self.project,
            date=date(2026, 5, 16),
            hours=7.5
        )
        self.assertEqual(TimeEntry.objects.count(), 1)
        self.assertEqual(str(entry), f"testuser - Test Project - 2026-05-16 (7.5h)")

    def test_unique_time_entry_per_day(self):
        TimeEntry.objects.create(
            user=self.user,
            project=self.project,
            date=date(2026, 5, 16),
            hours=8.0
        )
        # Ugyanarra a napra és projektre nem készülhet még egy külön bejegyzés
        with self.assertRaises(IntegrityError):
            TimeEntry.objects.create(
                user=self.user,
                project=self.project,
                date=date(2026, 5, 16),
                hours=2.0
            )

class TimesheetViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client_obj = Client.objects.create(name='Test Client')
        self.project = Project.objects.create(name='Test Project', client=self.client_obj)
        self.project.assigned_users.add(self.user)
        self.url = reverse('timesheet:index')
        self.api_url = reverse('timesheet:api_save')

    def test_timesheet_view_access(self):
        # Nincs belépve -> redirect
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

        # Belépve -> 200 OK
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'timesheet/index.html')

    def test_save_time_entry_api(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'project_id': self.project.id,
            'date': '2026-05-16',
            'hours': '6ó 30p'
        }
        response = self.client.post(self.api_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        resp_data = response.json()
        self.assertEqual(resp_data['status'], 'success')
        self.assertEqual(resp_data['formatted_hours'], '6ó 30p')
        
        # Ellenőrzés adatbázisban
        entry = TimeEntry.objects.get(user=self.user, project=self.project, date=date(2026, 5, 16))
        self.assertEqual(entry.hours, 6.5)

    def test_delete_time_entry_api_zero_hours(self):
        self.client.login(username='testuser', password='password123')
        # Létrehozunk egyet először
        TimeEntry.objects.create(user=self.user, project=self.project, date=date(2026, 5, 16), hours=8.0)
        
        # Most 0-t küldünk rá, hogy törlődjön
        data = {
            'project_id': self.project.id,
            'date': '2026-05-16',
            'hours': '0'
        }
        response = self.client.post(self.api_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TimeEntry.objects.count(), 0)

