from django.shortcuts import render, get_object_or_404

from .models import Person


def view_family_tree(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    return render(request, 'member/family_tree.html', {'family_tree': [person]})