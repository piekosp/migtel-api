from django.db import models

from users.models import User


class PolishClassificationOfActivities(models.Model):
    section = models.CharField(max_length=1)
    department = models.CharField(max_length=2)
    group = models.CharField(max_length=5)
    industry = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.group} - {self.industry}"


class Company(models.Model):
    nip = models.CharField(null=True, blank=True, unique=True, max_length=10)
    krs = models.CharField(null=True, blank=True, max_length=10)
    regon = models.CharField(null=True, blank=True, max_length=14)
    name = models.CharField(max_length=255)
    address1 = models.CharField(null=True, blank=True, max_length=60)
    address2 = models.CharField(null=True, blank=True, max_length=20)
    zip = models.CharField(null=True, blank=True, max_length=6)
    city = models.CharField(null=True, blank=True, max_length=30)
    state = models.CharField(null=True, blank=True, max_length=30)
    phone1 = models.CharField(null=True, blank=True, max_length=14)
    phone2 = models.CharField(null=True, blank=True, max_length=14)
    email1 = models.CharField(null=True, blank=True, max_length=60)
    email2 = models.CharField(null=True, blank=True, max_length=60)
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

    def __str__(self):
        return self.name


class CsvFile(models.Model):
    file = models.FileField(upload_to="companies/")

    def __str__(self):
        return str(self.file)


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    criteria = models.JSONField()


class CompanyStatus(models.Model):
    company = models.OneToOneField(
        Company, on_delete=models.CASCADE, primary_key=True, related_name="status"
    )
    assigned_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    taken = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    completed_on = models.DateField(null=True)
