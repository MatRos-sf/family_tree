from django.db import models

class Person(models.Model):
    GENDER_CHOICE = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    # personal data
    name = models.CharField(max_length=70)
    second_name = models.CharField(max_length=100)
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


    def __str__(self):
        return f"{self.name} {self.second_name}"

    def siblings(self):
        """
        return Siblings ( sisters or brothers) share the same biological parents.
        """
        sibling = Person.objects.filter(mother=self.mother, father=self.father).exclude(id=self.id)
        return sibling

    def half_siblings(self):
        ...


#Probant: w genealogii to osoba: która zajmuje centralne miejsce na tablicy genealogicznej, lub dla której
# oblicza się stopień pokrewieństwa, lub wobec której określa się nazwę relacji rodzinnej. w genetyce – osoba, która jest przedmiotem badania