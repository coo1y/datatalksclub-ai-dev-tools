from functools import wraps

from django.shortcuts import redirect

from .models import Person

SESSION_KEY = 'person_id'


def get_current_person(request):
    person_id = request.session.get(SESSION_KEY)
    if not person_id:
        return None
    return Person.objects.filter(pk=person_id, is_active=True).first()


def require_person(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if get_current_person(request) is None:
            return redirect('chores:login')
        return view_func(request, *args, **kwargs)

    return wrapper
