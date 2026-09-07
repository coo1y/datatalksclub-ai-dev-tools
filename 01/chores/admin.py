from django.contrib import admin

from .models import Chore, Person, Week


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ('start_date',)


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'week', 'assigned_to', 'completed', 'completed_by', 'completed_at')
    list_filter = ('week', 'completed', 'assigned_to')
    search_fields = ('name',)
