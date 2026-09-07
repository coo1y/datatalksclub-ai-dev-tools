from django import forms

from .models import Chore, Person


class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ['name', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = Person.objects.filter(is_active=True)
