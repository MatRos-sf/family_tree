from django.test import TestCase
from datetime import datetime


from .models_test import create_fake_person_payload
from member.models import Person

class PersonTest(TestCase):

    def test_check_oldest_ancestor(self):
        person_one = Person.objects.create(**create_fake_person_payload(blood_main_family=True))
        person_one = Person.objects.create(**create_fake_person_payload(blood_main_family=True))