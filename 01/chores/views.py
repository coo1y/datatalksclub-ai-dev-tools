from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .decorators import SESSION_KEY, get_current_person, require_person
from .forms import ChoreForm
from .models import Chore, Person, Week

LOGIN_MAX_ATTEMPTS = 5
LOGIN_LOCKOUT_SECONDS = 60


def get_current_week():
    return Week.objects.order_by('-start_date').first()


def home_view(request):
    current_week = get_current_week()
    chores = (
        current_week.chores.select_related('assigned_to', 'completed_by') if current_week else []
    )
    return render(request, 'chores/home.html', {
        'current_week': current_week,
        'chores': chores,
    })


def login_view(request):
    if request.method == 'POST':
        person = Person.objects.filter(pk=request.POST.get('person_id'), is_active=True).first()
        attempts_key = f'login_attempts_{request.POST.get("person_id")}'

        if person and cache.get(attempts_key, 0) >= LOGIN_MAX_ATTEMPTS:
            messages.error(request, 'Too many wrong PINs — try again in a minute.')
        elif person and person.check_pin(request.POST.get('pin', '')):
            cache.delete(attempts_key)
            request.session[SESSION_KEY] = person.pk
            return redirect('chores:home')
        else:
            if person:
                cache.set(attempts_key, cache.get(attempts_key, 0) + 1, LOGIN_LOCKOUT_SECONDS)
            messages.error(request, "That person or PIN wasn't recognized.")

    people = Person.objects.filter(is_active=True)
    return render(request, 'chores/login.html', {'people': people})


def logout_view(request):
    request.session.pop(SESSION_KEY, None)
    return redirect('chores:login')


def plan_view(request):
    current_week = get_current_week()
    chores = current_week.chores.select_related('assigned_to') if current_week else []
    started_today = bool(current_week and current_week.start_date == timezone.localdate())
    return render(request, 'chores/plan.html', {
        'current_week': current_week,
        'chores': chores,
        'form': ChoreForm(),
        'started_today': started_today,
    })


@require_person
def start_week_view(request):
    if request.method == 'POST':
        Week.objects.get_or_create(start_date=timezone.localdate())
    return redirect('chores:plan')


@require_person
def add_chore_view(request):
    current_week = get_current_week()
    if current_week is None:
        messages.error(request, 'Start a week before adding chores.')
        return redirect('chores:plan')

    if request.method == 'POST':
        form = ChoreForm(request.POST)
        if form.is_valid():
            chore = form.save(commit=False)
            chore.week = current_week
            chore.save()
        else:
            messages.error(request, 'Could not add that chore — check the name and assignee.')
    return redirect('chores:plan')


@require_person
def edit_chore_view(request, chore_id):
    chore = get_object_or_404(Chore, pk=chore_id, week=get_current_week())
    if request.method == 'POST':
        form = ChoreForm(request.POST, instance=chore)
        if form.is_valid():
            form.save()
            return redirect('chores:plan')
    else:
        form = ChoreForm(instance=chore)
    return render(request, 'chores/edit_chore.html', {'form': form, 'chore': chore})


@require_person
def delete_chore_view(request, chore_id):
    chore = get_object_or_404(Chore, pk=chore_id, week=get_current_week())
    if request.method == 'POST':
        chore.delete()
    return redirect('chores:plan')


@require_person
def toggle_chore_view(request, chore_id):
    chore = get_object_or_404(Chore, pk=chore_id, week=get_current_week())
    if request.method == 'POST':
        if chore.completed:
            chore.completed = False
            chore.completed_by = None
            chore.completed_at = None
        else:
            chore.completed = True
            chore.completed_by = get_current_person(request)
            chore.completed_at = timezone.now()
        chore.save()
    return redirect('chores:home')


def history_view(request):
    weeks = Week.objects.all()
    return render(request, 'chores/history.html', {'weeks': weeks})


def week_detail_view(request, week_id):
    week = get_object_or_404(Week, pk=week_id)
    chores = week.chores.select_related('assigned_to', 'completed_by')
    return render(request, 'chores/week_detail.html', {'week': week, 'chores': chores})
