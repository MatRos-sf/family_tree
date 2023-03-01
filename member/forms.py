from django import forms

from .models import Person

class PersonForm(forms.ModelForm):
    #birth = forms.DateField(required=False)
    class Meta:
        model = Person
        fields = '__all__'
        # fields = ['forename', 'middle_name', 'second_name', 'maiden_name', 'birth', 'death_date',
        #           'gender', 'history', 'mother', 'father', 'partner', 'blood_main_family', 'is_oldest_ancestor',
        #           'is_check']
