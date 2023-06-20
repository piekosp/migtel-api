from django.db import models


class State(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=19)


class PolishClassificationOfActivities(models.Model):
    section = models.CharField(max_length=1)
    department = models.CharField(max_length=2)
    group = models.CharField(max_length=5)
    industry = models.CharField(max_length=255)


class LegalForm(models.Model):
    basic = models.CharField(max_length=1)
    specific = models.CharField(max_length=3)


class Company(models.Model):
    nip = models.CharField(null=True, blank=True, unique=True, max_length=10)
    krs = models.CharField(null=True, blank=True, unique=True, max_length=10)
    regon = models.CharField(null=True, blank=True, unique=True, max_length=14)
    name = models.CharField(max_length=255)
    address1 = models.CharField(null=True, blank=True, max_length=60)
    address2 = models.CharField(null=True, blank=True, max_length=10)
    zip = models.CharField(null=True, blank=True, max_length=6)
    city = models.CharField(null=True, blank=True, max_length=30)
    state = models.ForeignKey(
        State, blank=True, null=True, default=None, on_delete=models.SET_NULL
    )
    website = models.CharField(blank=True, null=True, max_length=100)
    facebook = models.CharField(blank=True, null=True, max_length=100)
    linkedin = models.CharField(blank=True, null=True, max_length=100)
    pca = models.ForeignKey(
        PolishClassificationOfActivities,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    employment_range = models.IntegerField()
    ownership_form = models.CharField(max_length=3)
    establishment_date = models.DateField()
    start_date = models.DateField()


class Phone(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="phone")
    number = models.CharField(max_length=14)


class Email(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="email")
    address = models.CharField(max_length=60)
