from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Q


class Person(models.Model):
    GENDER_CHOICE = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    # personal data
    forename = models.CharField(max_length=70)
    middle_name = models.CharField(max_length=70, null=True, blank=True)
    second_name = models.CharField(max_length=100)
    maiden_name = models.CharField(max_length=100, null=True, blank=True)

    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    is_life = models.BooleanField(default=True)

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICE,
        default='M'
    )
    history = models.TextField(null=True, blank=True)
    mother = models.ForeignKey('self', related_name="mother_of_children",
                               on_delete= models.SET_NULL, null=True, blank=True)
    father = models.ForeignKey('self', related_name="father_of_children",
                               on_delete= models.SET_NULL, null=True, blank=True)
    partner = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    blood_main_family = models.BooleanField(default=True)

    is_oldest_ancestor = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    is_check = models.BooleanField(default=False)

    image_profile = models.ImageField(default='default.png')

    def __str__(self):
        return self.forename + ' ' + self.second_name

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    def clean(self):
        if self.is_oldest_ancestor:
            existing = Person.objects.filter(is_oldest_ancestor=True)
            if existing.exists() and existing.first().id != self.id:
                raise ValidationError("Only one instance can have is_oldest_ancestor=True")

    def get_siblings(self):
        """
        return Siblings ( sisters or brothers) share the same biological parents.
        """
        if self.mother and self.father:
            sibling = Person.objects.filter(mother=self.mother, father=self.father).exclude(id=self.id)
        else:
            return None
        return sibling

    def count_siblings(self) -> int:
        """ Count only siblings share the same biological parents"""
        siblings = self.get_siblings()
        return siblings.count() if siblings else 0

    def half_siblings(self):
        return Person.objects.filter(~Q(id=self.id), Q(~Q(father=None), ~Q(mother=self.mother), father=self.father) |\
                                     Q(~Q(mother=None), ~Q(father=self.father), mother=self.mother))

    def count_half_siblings(self):
        return self.half_siblings().count()

    def count_all_siblings(self):
        return sum((self.count_siblings(), self.count_half_siblings()))
    def grandparents_mother_side(self):
        """
        Grandparents mother side
        """
        grandparents = []
        if self.mother:
            grandma = self.mother.mother
            grandpa = self.mother.father
            if grandma:     grandparents.append(grandma)
            if grandpa:     grandparents.append(grandpa)
        else:
            None
        return grandparents

    def grandparents_father_side(self):
        """
        Grandparents father side
        """
        grandparents = []
        if self.father:
            grandma = self.mother.mother
            grandpa = self.mother.father
            if grandma:     grandparents.append(grandma)
            if grandpa:     grandparents.append(grandpa)
        return grandparents

    def name(self):
        " name_middleName_second_name_(maiden_name)"
        maiden_name = " (" + self.maiden_name + ")" if self.maiden_name else None
        return f"{self.forename} {self.middle_name if self.middle_name else ''} {self.second_name}"+f"{maiden_name if maiden_name else ''}"

    def count_children(self):
        children = self.father_of_children.count()
        return children

    def get_children(self):
        return Person.objects.filter(Q(mother=self) | Q(father=self))

    def count_grandchildren(self):
        children = self.father_of_children.all()
        grandchildren = 0
        for child in children:
            grandchildren += child.count_children()

        return grandchildren

    def check_is_life(self):
        """Check person is life"""
        if self.is_life and self.death_date:
            self.is_life = False
        return self.is_life




#Probant: w genealogii to osoba: która zajmuje centralne miejsce na tablicy genealogicznej, lub dla której
# oblicza się stopień pokrewieństwa, lub wobec której określa się nazwę relacji rodzinnej. w genetyce – osoba, która jest przedmiotem badania