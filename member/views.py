from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from django.db.models import Q


from .models import Person
from .forms import PersonForm

## CRUD
class CreatePersonView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'member/member_create.html'

class DetailPersonView(DetailView):
    model = Person
    template_name = 'member/member_detail.html'

class DeletePersonView(DeleteView):

    model = Person
    success_url = reverse_lazy('home')
    template_name = 'member/member_confirm_delete.html'

class UpdatePersonView(UpdateView):

    model = Person
    form_class = PersonForm
    template_name = 'member/member_create.html'


def view_family_tree(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    return render(request, 'member/family_tree.html', {'family_tree': [person]})

def home(request):
    return render(request, "member/home_page.html")

class SearchResultView(ListView):

    model = Person
    template_name = 'member/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Person.objects.filter(Q(name__icontains=query) | Q(second_name__icontains=query))
        return object_list

def find_oldest_ancestor(person):

    oldest = None

    if person.father and person.father.blood_main_family:
        oldest = person.father
    elif person.mother and person.mother.blood_main_family:
        oldest = person.mother

    if oldest:
        oldest = find_oldest_ancestor(oldest)
    else:
        oldest = person
    return oldest

def check_oldest_ancestor(request):

    # Check is Person on db
    if Person.objects.count() == 0:
        text = "We don't have any person on our Database! Please add."
        return HttpResponse(text)

    try:
        person = Person.objects.get(is_oldest_ancestor=True)
    except ObjectDoesNotExist:
        person = None
    if person:
        # check person have any parents just in case
        father = person.father
        mother = person.mother
        if not father and not mother:
            text = f"<h1>The oldest ancestor is {person.__str__()}"
            return HttpResponse(text)
        else:
            # find oldest person
            print(f"Now oldest: {person}")
            oldest_person = find_oldest_ancestor(person)
            person.is_oldest_ancestor = False
            person.save()
            oldest_person.is_oldest_ancestor = True
            oldest_person.save()
            print(f"New oldest {oldest_person}")
            text = f"<h1>The oldest ancestor is {oldest_person}"
            return HttpResponse(text)
    else:

        person = Person.objects.filter(blood_main_family=True).order_by('?')
        oldest_person = find_oldest_ancestor(person.first())
        oldest_person.is_oldest_ancestor = True
        oldest_person.save()
        text = f"<h1>The oldest ancestor is {oldest_person}"
        return HttpResponse(text)


