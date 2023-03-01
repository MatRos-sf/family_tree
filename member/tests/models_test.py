from django.test import TestCase
from datetime import datetime

from faker import Faker

from member.models import Person

def create_fake_person_payload(**kwargs):
    faker = Faker()
    fullname = faker.name().split(' ', 2)
    payload = {
        'forename': fullname[0],
        'second_name': fullname[1],
        'birth_date': faker.date_of_birth(),
        'gender': faker.random_element(['M', 'F']),
    }
    return {**payload, **kwargs}


class PersonTest(TestCase):
    def setUp(self) -> None:
        self.person = Person.objects.create( **create_fake_person_payload(
            forename = 'name_test',
            second_name='second_name_test',
            birth_date = datetime.strptime('2000-01-01', "%Y-%m-%d"),
            gender='M'
        ))

    def test_person_create(self):
        self.assertTrue(isinstance(self.person, Person))
        self.assertEqual(self.person.forename, 'name_test')
        self.assertEqual(self.person.birth_date.strftime('%Y-%m-%d'), '2000-01-01')

    def test_generate_fake_person(self):
        # generate fake person
        for i in range(9):
            Person.objects.create(
                ** create_fake_person_payload()
            )

        self.assertEqual(Person.objects.count(), 10)

    def test_siblings(self):
        # create parents
        mother = Person.objects.create( **create_fake_person_payload(
            gender='F',
            blood_main_family=False
        ))
        father = Person.objects.create( **create_fake_person_payload(
            gender='M'
        ))

        self.person.mother = mother
        self.person.father = father
        self.person.save()

        self.assertEqual(self.person.count_siblings(), 0)

        #create siblings
        s1 = Person.objects.create(
            **create_fake_person_payload(
            mother=mother,
            father=father,
            )
        )
        s2 = Person.objects.create(
            **create_fake_person_payload(
            mother=mother,
            father=father,
            )
        )

        self.assertEqual(self.person.count_siblings(), 2)

    def test_no_siblings(self):
        # create probant
        proband = Person.objects.create(**create_fake_person_payload())
        # create parents
        mother = Person.objects.create(**create_fake_person_payload(blood_main_family=False))

        father = Person.objects.create(
            **create_fake_person_payload(
            gender='M'
            )
        )
        #create siblings
        s1 = Person.objects.create(
            **create_fake_person_payload(
            gender='M',
            mother=mother,
            )
        )

        proband.mother, proband.father = mother, father
        proband.save()

        self.assertEqual(proband.count_siblings(), 0)

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

    def test_half_siblings(self):

        mother = Person.objects.create(**create_fake_person_payload(gender='F'))
        father = Person.objects.create(**create_fake_person_payload(gender='M'))

        probant = Person.objects.create(**create_fake_person_payload(mother=mother, father=father))

        # create only father childs
        father_child_one = Person.objects.create(**create_fake_person_payload(forename='Ala',father=father))
        father_child_two = Person.objects.create(**create_fake_person_payload(forename='Tom',father=father))

        # create only mother child
        mother_child_one = Person.objects.create(**create_fake_person_payload(forename='Ash',mother=mother))

        # create common child
        common_child = Person.objects.create(**create_fake_person_payload(forename='Mat', mother=mother, father=father))

        self.assertEqual(probant.count_half_siblings() , 3)

        half_brother = probant.half_siblings()

        self.assertFalse(half_brother.filter(id=common_child.id))
        self.assertTrue(half_brother.filter(id=mother_child_one.id))

        self.assertEqual(probant.count_all_siblings(), 4)

        #self.assertFalse(half_brother.exist)

    def test_count_own_children(self):
        father = Person.objects.create(**create_fake_person_payload())

        for child in range(5):
            c = Person.objects.create(**create_fake_person_payload(father=father, gender='M'))
            for grandchildren in range(2):
                Person.objects.create(**create_fake_person_payload(father=c))
        self.assertEqual(father.count_children(), 5)
        self.assertEqual(father.count_grandchildren(), 10)
