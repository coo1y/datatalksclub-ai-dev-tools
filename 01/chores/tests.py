from datetime import timedelta
from io import StringIO

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .decorators import SESSION_KEY
from .forms import ChoreForm
from .models import Chore, Person, Week
from .views import LOGIN_MAX_ATTEMPTS


class PersonModelTests(TestCase):
    def test_set_pin_hashes_and_check_pin_validates(self):
        person = Person(name='Alex')
        person.set_pin('4242')
        person.save()
        self.assertNotEqual(person.pin_hash, '4242')
        self.assertTrue(person.check_pin('4242'))
        self.assertFalse(person.check_pin('0000'))


class WeekModelTests(TestCase):
    def test_str_includes_start_date(self):
        week = Week.objects.create(start_date=timezone.localdate())
        self.assertIn(str(timezone.localdate()), str(week))

    def test_default_ordering_is_most_recent_first(self):
        older = Week.objects.create(start_date=timezone.localdate() - timedelta(days=7))
        newer = Week.objects.create(start_date=timezone.localdate())
        self.assertEqual(list(Week.objects.all()), [newer, older])


class ChoreModelTests(TestCase):
    def setUp(self):
        self.person = Person(name='Alex')
        self.person.set_pin('4242')
        self.person.save()
        self.week = Week.objects.create()

    def test_new_chore_defaults_to_not_completed(self):
        chore = Chore.objects.create(week=self.week, name='Dishes', assigned_to=self.person)
        self.assertFalse(chore.completed)
        self.assertIsNone(chore.completed_by)
        self.assertIsNone(chore.completed_at)

    def test_completing_a_chore_records_person_and_timestamp(self):
        chore = Chore.objects.create(week=self.week, name='Dishes', assigned_to=self.person)
        now = timezone.now()
        chore.completed = True
        chore.completed_by = self.person
        chore.completed_at = now
        chore.save()

        chore.refresh_from_db()
        self.assertTrue(chore.completed)
        self.assertEqual(chore.completed_by, self.person)
        self.assertEqual(chore.completed_at, now)


class LoginFlowTests(TestCase):
    def setUp(self):
        self.person = Person(name='Alex')
        self.person.set_pin('4242')
        self.person.save()
        cache.clear()

    def test_home_accessible_without_login(self):
        response = self.client.get(reverse('chores:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')

    def test_wrong_pin_does_not_log_in(self):
        response = self.client.post(
            reverse('chores:login'), {'person_id': self.person.pk, 'pin': '0000'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_correct_pin_logs_in(self):
        response = self.client.post(
            reverse('chores:login'),
            {'person_id': self.person.pk, 'pin': '4242'},
            follow=True,
        )
        self.assertEqual(self.client.session.get(SESSION_KEY), self.person.pk)
        self.assertContains(response, 'Alex')

    def test_logout_clears_session(self):
        self.client.post(reverse('chores:login'), {'person_id': self.person.pk, 'pin': '4242'})
        self.assertEqual(self.client.session.get(SESSION_KEY), self.person.pk)
        response = self.client.get(reverse('chores:logout'), follow=True)
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertContains(response, 'Log in')

    def test_lockout_after_too_many_wrong_pins(self):
        for _ in range(LOGIN_MAX_ATTEMPTS):
            self.client.post(reverse('chores:login'), {'person_id': self.person.pk, 'pin': '0000'})

        response = self.client.post(
            reverse('chores:login'), {'person_id': self.person.pk, 'pin': '4242'}
        )
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertContains(response, 'Too many wrong PINs')

    def test_successful_login_resets_attempt_counter(self):
        for _ in range(LOGIN_MAX_ATTEMPTS - 1):
            self.client.post(reverse('chores:login'), {'person_id': self.person.pk, 'pin': '0000'})

        self.client.post(reverse('chores:login'), {'person_id': self.person.pk, 'pin': '4242'})
        self.assertEqual(self.client.session.get(SESSION_KEY), self.person.pk)

        self.client.get(reverse('chores:logout'))
        response = self.client.post(
            reverse('chores:login'), {'person_id': self.person.pk, 'pin': '4242'}, follow=True
        )
        self.assertEqual(self.client.session.get(SESSION_KEY), self.person.pk)
        self.assertContains(response, 'Alex')


class WeeklyPlanningTests(TestCase):
    def setUp(self):
        cache.clear()
        self.person = Person(name='Alex')
        self.person.set_pin('4242')
        self.person.save()

    def log_in(self):
        self.client.post(reverse('chores:login'), {'person_id': self.person.pk, 'pin': '4242'})

    def test_start_week_requires_login(self):
        response = self.client.post(reverse('chores:start_week'))
        self.assertRedirects(response, reverse('chores:login'))
        self.assertEqual(Week.objects.count(), 0)

    def test_start_week_creates_week_for_today(self):
        self.log_in()
        self.client.post(reverse('chores:start_week'))
        self.assertEqual(Week.objects.count(), 1)
        self.assertEqual(Week.objects.first().start_date, timezone.localdate())

    def test_start_week_does_not_duplicate_todays_week(self):
        self.log_in()
        self.client.post(reverse('chores:start_week'))
        self.client.post(reverse('chores:start_week'))
        self.assertEqual(Week.objects.count(), 1)

    def test_add_chore_requires_login(self):
        Week.objects.create()
        response = self.client.post(
            reverse('chores:add_chore'), {'name': 'Dishes', 'assigned_to': self.person.pk}
        )
        self.assertRedirects(response, reverse('chores:login'))
        self.assertEqual(Chore.objects.count(), 0)

    def test_add_chore_attaches_to_current_week(self):
        self.log_in()
        week = Week.objects.create()
        self.client.post(
            reverse('chores:add_chore'), {'name': 'Dishes', 'assigned_to': self.person.pk}
        )
        chore = Chore.objects.get()
        self.assertEqual(chore.week, week)
        self.assertEqual(chore.name, 'Dishes')
        self.assertEqual(chore.assigned_to, self.person)

    def test_add_chore_without_week_shows_error(self):
        self.log_in()
        response = self.client.post(
            reverse('chores:add_chore'),
            {'name': 'Dishes', 'assigned_to': self.person.pk},
            follow=True,
        )
        self.assertEqual(Chore.objects.count(), 0)
        self.assertContains(response, 'Start a week')

    def test_edit_chore_updates_fields(self):
        self.log_in()
        week = Week.objects.create()
        chore = Chore.objects.create(week=week, name='Dishes', assigned_to=self.person)
        other = Person(name='Sam')
        other.set_pin('1111')
        other.save()
        self.client.post(
            reverse('chores:edit_chore', args=[chore.pk]),
            {'name': 'Laundry', 'assigned_to': other.pk},
        )
        chore.refresh_from_db()
        self.assertEqual(chore.name, 'Laundry')
        self.assertEqual(chore.assigned_to, other)

    def test_delete_chore_removes_it(self):
        self.log_in()
        week = Week.objects.create()
        chore = Chore.objects.create(week=week, name='Dishes', assigned_to=self.person)
        self.client.post(reverse('chores:delete_chore', args=[chore.pk]))
        self.assertEqual(Chore.objects.count(), 0)

    def test_plan_view_shows_chores(self):
        week = Week.objects.create()
        Chore.objects.create(week=week, name='Dishes', assigned_to=self.person)
        response = self.client.get(reverse('chores:plan'))
        self.assertContains(response, 'Dishes')
        self.assertContains(response, 'Alex')


class DailyUseTests(TestCase):
    def setUp(self):
        cache.clear()
        self.person = Person(name='Alex')
        self.person.set_pin('4242')
        self.person.save()
        self.week = Week.objects.create()
        self.chore = Chore.objects.create(week=self.week, name='Dishes', assigned_to=self.person)

    def log_in(self):
        self.client.post(reverse('chores:login'), {'person_id': self.person.pk, 'pin': '4242'})

    def test_current_week_visible_without_login(self):
        response = self.client.get(reverse('chores:home'))
        self.assertContains(response, 'Dishes')
        self.assertContains(response, 'Not done')

    def test_toggle_requires_login(self):
        response = self.client.post(reverse('chores:toggle_chore', args=[self.chore.pk]))
        self.assertRedirects(response, reverse('chores:login'))
        self.chore.refresh_from_db()
        self.assertFalse(self.chore.completed)

    def test_toggle_marks_complete_with_person_and_time(self):
        self.log_in()
        self.client.post(reverse('chores:toggle_chore', args=[self.chore.pk]))
        self.chore.refresh_from_db()
        self.assertTrue(self.chore.completed)
        self.assertEqual(self.chore.completed_by, self.person)
        self.assertIsNotNone(self.chore.completed_at)

    def test_toggle_again_marks_incomplete(self):
        self.log_in()
        self.client.post(reverse('chores:toggle_chore', args=[self.chore.pk]))
        self.client.post(reverse('chores:toggle_chore', args=[self.chore.pk]))
        self.chore.refresh_from_db()
        self.assertFalse(self.chore.completed)
        self.assertIsNone(self.chore.completed_by)
        self.assertIsNone(self.chore.completed_at)

    def test_any_logged_in_person_can_toggle_anyones_chore(self):
        other = Person(name='Sam')
        other.set_pin('1111')
        other.save()
        self.client.post(reverse('chores:login'), {'person_id': other.pk, 'pin': '1111'})
        self.client.post(reverse('chores:toggle_chore', args=[self.chore.pk]))
        self.chore.refresh_from_db()
        self.assertTrue(self.chore.completed)
        self.assertEqual(self.chore.completed_by, other)


class HistoryTests(TestCase):
    def setUp(self):
        self.person = Person(name='Alex')
        self.person.set_pin('4242')
        self.person.save()
        self.old_week = Week.objects.create(start_date=timezone.localdate() - timedelta(days=14))
        self.new_week = Week.objects.create(start_date=timezone.localdate())
        self.done_chore = Chore.objects.create(
            week=self.old_week,
            name='Dishes',
            assigned_to=self.person,
            completed=True,
            completed_by=self.person,
            completed_at=timezone.now(),
        )
        self.missed_chore = Chore.objects.create(
            week=self.old_week, name='Laundry', assigned_to=self.person
        )

    def test_history_accessible_without_login(self):
        response = self.client.get(reverse('chores:history'))
        self.assertEqual(response.status_code, 200)

    def test_history_lists_weeks_most_recent_first(self):
        response = self.client.get(reverse('chores:history'))
        content = response.content.decode()
        self.assertLess(content.index(str(self.new_week)), content.index(str(self.old_week)))

    def test_week_detail_shows_done_and_missed_status(self):
        response = self.client.get(reverse('chores:week_detail', args=[self.old_week.pk]))
        self.assertContains(response, 'Dishes')
        self.assertContains(response, 'Done by Alex')
        self.assertContains(response, 'Laundry')
        self.assertContains(response, 'Missed')

    def test_week_detail_has_no_edit_controls(self):
        response = self.client.get(reverse('chores:week_detail', args=[self.old_week.pk]))
        self.assertNotContains(response, 'Mark done')
        self.assertNotContains(response, 'Delete')
        self.assertNotContains(response, '<form')


class AccessControlTests(TestCase):
    def setUp(self):
        cache.clear()
        self.person = Person(name='Alex')
        self.person.set_pin('4242')
        self.person.save()
        self.inactive = Person(name='Retired', is_active=False)
        self.inactive.set_pin('9999')
        self.inactive.save()

    def log_in(self):
        self.client.post(reverse('chores:login'), {'person_id': self.person.pk, 'pin': '4242'})

    def test_inactive_person_cannot_log_in(self):
        response = self.client.post(
            reverse('chores:login'), {'person_id': self.inactive.pk, 'pin': '9999'}
        )
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertContains(response, 'recognized')

    def test_inactive_person_not_offered_on_login_page(self):
        response = self.client.get(reverse('chores:login'))
        self.assertNotContains(response, 'Retired')

    def test_past_week_chore_cannot_be_edited(self):
        past_week = Week.objects.create(start_date=timezone.localdate() - timedelta(days=7))
        Week.objects.create(start_date=timezone.localdate())  # now the current week
        chore = Chore.objects.create(week=past_week, name='Dishes', assigned_to=self.person)

        self.log_in()
        response = self.client.post(
            reverse('chores:edit_chore', args=[chore.pk]),
            {'name': 'Changed', 'assigned_to': self.person.pk},
        )
        self.assertEqual(response.status_code, 404)
        chore.refresh_from_db()
        self.assertEqual(chore.name, 'Dishes')

    def test_past_week_chore_cannot_be_deleted(self):
        past_week = Week.objects.create(start_date=timezone.localdate() - timedelta(days=7))
        Week.objects.create(start_date=timezone.localdate())
        chore = Chore.objects.create(week=past_week, name='Dishes', assigned_to=self.person)

        self.log_in()
        response = self.client.post(reverse('chores:delete_chore', args=[chore.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Chore.objects.filter(pk=chore.pk).exists())

    def test_past_week_chore_cannot_be_toggled(self):
        past_week = Week.objects.create(start_date=timezone.localdate() - timedelta(days=7))
        Week.objects.create(start_date=timezone.localdate())
        chore = Chore.objects.create(week=past_week, name='Dishes', assigned_to=self.person)

        self.log_in()
        response = self.client.post(reverse('chores:toggle_chore', args=[chore.pk]))
        self.assertEqual(response.status_code, 404)
        chore.refresh_from_db()
        self.assertFalse(chore.completed)

    def test_lockout_is_scoped_per_person(self):
        other = Person(name='Sam')
        other.set_pin('1111')
        other.save()

        for _ in range(LOGIN_MAX_ATTEMPTS):
            self.client.post(reverse('chores:login'), {'person_id': self.person.pk, 'pin': '0000'})

        response = self.client.post(
            reverse('chores:login'), {'person_id': other.pk, 'pin': '1111'}, follow=True
        )
        self.assertEqual(self.client.session.get(SESSION_KEY), other.pk)
        self.assertContains(response, 'Sam')


class FormValidationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.person = Person(name='Alex')
        self.person.set_pin('4242')
        self.person.save()
        self.week = Week.objects.create()

    def log_in(self):
        self.client.post(reverse('chores:login'), {'person_id': self.person.pk, 'pin': '4242'})

    def test_blank_chore_name_is_rejected(self):
        self.log_in()
        response = self.client.post(
            reverse('chores:add_chore'), {'name': '', 'assigned_to': self.person.pk}, follow=True
        )
        self.assertEqual(Chore.objects.count(), 0)
        self.assertContains(response, 'Could not add that chore')

    def test_inactive_person_excluded_from_assignee_choices(self):
        inactive = Person(name='Retired', is_active=False)
        inactive.set_pin('9999')
        inactive.save()

        form = ChoreForm()
        self.assertNotIn(inactive, form.fields['assigned_to'].queryset)
        self.assertIn(self.person, form.fields['assigned_to'].queryset)


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.force_login(self.admin_user)

    def test_person_admin_list_view(self):
        response = self.client.get(reverse('admin:chores_person_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_week_admin_list_view(self):
        response = self.client.get(reverse('admin:chores_week_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_chore_admin_list_view(self):
        response = self.client.get(reverse('admin:chores_chore_changelist'))
        self.assertEqual(response.status_code, 200)


class SeedDemoDataCommandTests(TestCase):
    def test_seed_creates_expected_records(self):
        call_command('seed_demo_data', stdout=StringIO())
        self.assertEqual(Person.objects.count(), 3)
        self.assertEqual(Week.objects.count(), 1)
        self.assertEqual(Chore.objects.count(), 4)

    def test_seed_is_idempotent(self):
        out = StringIO()
        call_command('seed_demo_data', stdout=out)
        call_command('seed_demo_data', stdout=out)
        self.assertEqual(Person.objects.count(), 3)
        self.assertEqual(Week.objects.count(), 1)
        self.assertEqual(Chore.objects.count(), 4)
