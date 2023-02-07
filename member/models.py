from django.db import models
from django.core.exceptions import ValidationError


class Person(models.Model):
    GENDER_CHOICE = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    # personal data
    name = models.CharField(max_length=70)
    second_name = models.CharField(max_length=100)
    maiden_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
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

    def __str__(self):
        #return f"{self.name} {self.second_name}"
        return self.aka()

    def clean(self):
        if self.is_oldest_ancestor:
            existing = Person.objects.filter(is_oldest_ancestor=True)
            if existing.exists() and existing.first().id != self.id:
                raise ValidationError("Only one instance can have is_oldest_ancestor=True")

    def siblings(self):
        """
        return Siblings ( sisters or brothers) share the same biological parents.
        """
        sibling = Person.objects.filter(mother=self.mother, father=self.father).exclude(id=self.id)
        return sibling

    def half_siblings(self):
        ...

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

    def aka(self):
        """

        """
        aka_text = f"{self.name} {self.second_name}:"
        father = self.father

        for _ in range(3):
            if father:
                aka_text += f" {father.name}"
                father = father.father
            else:
                break

        return aka_text





#Probant: w genealogii to osoba: która zajmuje centralne miejsce na tablicy genealogicznej, lub dla której
# oblicza się stopień pokrewieństwa, lub wobec której określa się nazwę relacji rodzinnej. w genetyce – osoba, która jest przedmiotem badania