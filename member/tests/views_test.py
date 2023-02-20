from django.urls import reverse
from django.test import TestCase, Client
from django.test.client import RequestFactory

from .models_test import create_fake_person_payload
from member.models import Person
from member.forms import PersonForm
from member.views import CreatePersonView, DetailPersonView, DeletePersonView

class PersonTest(TestCase):

    def test_check_oldest_ancestor(self):
        person_one = Person.objects.create(**create_fake_person_payload(blood_main_family=True))
        person_one = Person.objects.create(**create_fake_person_payload(blood_main_family=True))



# class CreatePersonViewTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     def test_create_person(self):
#         # Set up a POST request with form data
#         data = create_fake_person_payload()
#         request = self.factory.post(reverse('create'), data=data)
#
#         # Test that the view creates a new Person object
#         response = CreatePersonView.as_view()(request)
#         self.assertEqual(Person.objects.count(), 1)
#
#         # Test that the view redirects to the detail page for the new Person object
#         new_person = Person.objects.first()
#         expected_url = reverse('detail', kwargs={'pk': new_person.pk})
#         self.assertRedirects(response, new_person.get_absolute_url())


class DetailPersonViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.person = Person.objects.create(**create_fake_person_payload())

    def test_detail_person(self):
        # Set up a GET request for the detail page
        request = self.factory.get(reverse('detail', kwargs={'pk': self.person.pk}))

        # Test that the view returns the correct context
        response = DetailPersonView.as_view()(request, pk=self.person.pk)
        self.assertEqual(response.context_data['person'], self.person)

class DeletePersonViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = Person.objects.create(**create_fake_person_payload())

    def test_delete_person(self):
        # Set up a POST request to delete the Person object
        request = self.client.post(reverse('delete', kwargs={'pk': self.person.pk}))

        # Test that the view deletes the Person object and redirects to the success URL
        self.assertEqual(Person.objects.count(), 0)
        self.assertRedirects(request, reverse('home'))
