from .decorators import get_current_person


def current_person(request):
    return {'current_person': get_current_person(request)}
