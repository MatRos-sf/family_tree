from django.test import TestCase
from datetime import datetime

from faker import Faker

from member.models import Person

def create_fake_person_payload(**kwargs):
    faker = Faker()
    fullname = faker.name().split(' ', 2)
    payload = {
        'name': fullname[0],
        'second_name': fullname[1],
        'birth_date': faker.date_of_birth(),
        'gender': faker.random_element(['M', 'F']),
    }
    return {**payload, **kwargs}


class PersonTest(TestCase):
    def setUp(self) -> None:
        self.person = Person.objects.create(
            name = 'name_test',
            second_name='second_name_test',
            birth_date = datetime.strptime('2000-01-01', "%Y-%m-%d"),
            gender='M'
        )

    def test_person_create(self):
        self.assertTrue(isinstance(self.person, Person))
        self.assertEqual(self.person.name, 'name_test')
        self.assertEqual(self.person.birth_date.strftime('%Y-%m-%d'), '2000-01-01')

    def test_generate_fake_person(self):
        # generate fake person
        fake = Faker()
        for i in range(9):
            fullname = fake.name().split(' ',2)
            Person.objects.create(
                name=fullname[0],
                second_name = fullname[1],
                birth_date = fake.date_of_birth(),
                gender = fake.random_element(['M', 'F']),
                blood_main_family = fake.random_element([True, False]),
            )

        self.assertEqual(Person.objects.count(), 10)

    def test_siblings(self):
        faker = Faker()
        # create parents
        fullname = faker.name().split(' ', 2)
        mother = Person.objects.create(
            name=fullname[0],
            second_name=fullname[1],
            birth_date=faker.date_of_birth(),
            gender='F',
            blood_main_family=False
        )
        father = Person.objects.create(
            name=faker.first_name(),
            second_name=faker.last_name(),
            birth_date=faker.date_of_birth(),
            gender='M'

        )

        self.person.mother = mother
        self.person.father = father
        self.person.save()

        self.assertEqual(self.person.siblings().count(), 0)

        #create siblings
        s1 = Person.objects.create(
            name=faker.first_name(),
            second_name=faker.last_name(),
            birth_date=faker.date_of_birth(),
            gender='M',
            mother=mother,
            father=father,

        )
        s2 = Person.objects.create(
            name=faker.first_name(),
            second_name=faker.last_name(),
            birth_date=faker.date_of_birth(),
            gender='M',
            mother=mother,
            father=father,

        )

        self.assertEqual(self.person.siblings().count(), 2)

    def test_no_siblings(self):
        faker = Faker()
        # create probant
        proband = Person.objects.create(**create_fake_person_payload())
        # create parents
        mother = Person.objects.create(**create_fake_person_payload(blood_main_family=False))
        fullname = faker.name().split(' ', 2)

        father = Person.objects.create(
            name=faker.first_name(),
            second_name=faker.last_name(),
            birth_date=faker.date_of_birth(),
            gender='M'

        )
        #create siblings
        s1 = Person.objects.create(
            name=faker.first_name(),
            second_name=faker.last_name(),
            birth_date=faker.date_of_birth(),
            gender='M',
            mother=mother,
        )

        proband.mother, proband.father = mother, father
        proband.save()
        create_fake_person_payload(nos=True)
        self.assertEqual(proband.siblings().count(), 0)

    def test_check_grandparents(self):
        #only grandma
        grandma = Person.objects.create(**create_fake_person_payload())
        mother = Person.objects.create(**create_fake_person_payload(mother=grandma))
        probatan = Person.objects.create(**create_fake_person_payload(mother=mother))

        self.assertEqual(len(probatan.grandparents_mother_side()), 1)
        # grandma and grandpa
        grandpa = Person.objects.create(**create_fake_person_payload())
        mother.father = grandpa
        mother.save()

        self.assertEqual(len(probatan.grandparents_mother_side()), 2)

