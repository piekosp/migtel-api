from django.db import models


class PolishClassificationOfActivities(models.Model):
    section = models.CharField(max_length=1)
    department = models.CharField(max_length=2)
    group = models.CharField(max_length=5)


class Company(models.Model):
    nip = models.CharField(null=True, blank=True, unique=True, max_length=10)
    krs = models.CharField(null=True, blank=True, unique=True, max_length=10)
    regon = models.CharField(null=True, blank=True, unique=True, max_length=14)
    name = models.CharField(max_length=255)
    address1 = models.CharField(null=True, blank=True, max_length=60)
    address2 = models.CharField(null=True, blank=True, max_length=20)
    zip = models.CharField(null=True, blank=True, max_length=6)
    city = models.CharField(null=True, blank=True, max_length=30)
    state = models.CharField(null=True, blank=True, max_length=30)
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
    basic_legal_form = models.CharField(max_length=1, blank=True, null=True)
    specific_legal_form = models.CharField(max_length=3, blank=True, null=True)
    ownership_form = models.CharField(max_length=3, blank=True, null=True)
    establishment_date = models.DateField()
    start_date = models.DateField()


class Phone(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="phone")
    number = models.CharField(max_length=14)


class Email(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="email")
    address = models.CharField(max_length=60)


class CsvFile(models.Model):
    file = models.FileField(upload_to="companies/")

    def __str__(self):
        return str(self.file)
