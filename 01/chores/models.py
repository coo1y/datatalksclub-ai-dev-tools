from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True)
    pin_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def set_pin(self, raw_pin):
        self.pin_hash = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin_hash)


class Week(models.Model):
    start_date = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'Week of {self.start_date}'


class Chore(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='chores')
    name = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='assigned_chores')
    completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(
        Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_chores'
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.week})'
