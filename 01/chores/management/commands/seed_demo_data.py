from django.core.management.base import BaseCommand
from django.utils import timezone

from chores.models import Chore, Person, Week

PEOPLE = [
    ('Alex', '1111'),
    ('Sam', '2222'),
    ('Jordan', '3333'),
]

CHORES = [
    'Dishes',
    'Laundry',
    'Take out trash',
    'Vacuum living room',
]


class Command(BaseCommand):
    help = 'Creates a few sample people and a sample week of chores for local development.'

    def handle(self, *args, **options):
        people = []
        for name, pin in PEOPLE:
            person, created = Person.objects.get_or_create(name=name)
            if created:
                person.set_pin(pin)
                person.save()
            people.append(person)
            self.stdout.write(f'Person: {name} (PIN {pin}){"  [created]" if created else ""}')

        week, created = Week.objects.get_or_create(start_date=timezone.localdate())
        self.stdout.write(f'Week: {week}{"  [created]" if created else ""}')

        for index, name in enumerate(CHORES):
            assignee = people[index % len(people)]
            _chore, created = Chore.objects.get_or_create(
                week=week, name=name, defaults={'assigned_to': assignee}
            )
            self.stdout.write(f'Chore: {name}{"  [created]" if created else ""}')

        self.stdout.write(self.style.SUCCESS('Seed data ready.'))
