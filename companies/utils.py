from datetime import datetime

from .models import Company, Email, Phone, PolishClassificationOfActivities


class CompanyDataImporter:
    def __init__(self, row):
        self.row = row

    def extract_data(self):
        company = self.company

        for email in self.emails:
            email.company = company
            email.save()

        for phone in self.phones:
            phone.company = company
            phone.save()

        company.pca = self.pca
        company.save()

        return company

    @property
    def pca(self):
        try:
            pca_object = (
                PolishClassificationOfActivities.objects.get(group=self.row["PKD"])
                if self.row["PKD"]
                else None
            )
        except PolishClassificationOfActivities.DoesNotExist:
            pca_object = None

        return pca_object

    @property
    def phones(self):
        phones = list(filter(None, [self.row["Telefon1"], self.row["Telefon2"]]))
        return [Phone.objects.create(number=phone) for phone in phones]

    @property
    def emails(self):
        emails = list(filter(None, [self.row["Email1"], self.row["Email2"]]))
        return [Email.objects.create(address=email) for email in emails]

    @property
    def company(self):
        address2 = self.row["Budynek"]
        if address2 and self.row["Lokal"]:
            address2 += f"/{self.row['Lokal']}"

        time_format = "%Y%m%d"
        establishment_date = datetime.strptime(
            self.row["Data powstania"], time_format
        ).date()
        start_date = datetime.strptime(
            self.row["Data rozpoczęcia działalności"], time_format
        ).date()

        company_data = {
            "krs": self.row["KRS"],
            "regon": self.row["REGON"],
            "name": self.row["Nazwa"],
            "address1": self.row["Ulica"],
            "address2": address2,
            "zip": self.row["Kod pocztowy"],
            "city": self.row["Miejscowość"],
            "state": self.row["Województwo"],
            "website": self.row["Strona WWW"],
            "facebook": self.row["Facebook"],
            "linkedin": self.row["LinkedIn"],
            "employment_range": self.row["Przedział zatrudniena"],
            "basic_legal_form": self.row["Podstawowa forma prawna"],
            "specific_legal_form": self.row["Szczególna forma prawna"],
            "establishment_date": establishment_date,
            "start_date": start_date,
        }

        if self.row["NIP"]:
            company_object, _ = Company.objects.get_or_create(
                nip=self.row["NIP"], defaults=company_data
            )
        else:
            name = company_data.pop("name")
            company_object, _ = Company.objects.get_or_create(
                name=name, defaults=company_data
            )

        return company_object


class CompanyDataExporter:
    def __init__(self, data):
        self.data = data

    def get_headers(self):
        return [
            "NIP",
            "KRS",
            "REGON",
            "Nazwa",
            "Adres1",
            "Adres2",
            "Kod pocztowy",
            "Miejscowość",
            "Województwo",
            "Strona WWW",
            "Facebook",
            "LinkedIn",
            "Przedział zatrudnienia",
            "Podstawowa forma prawna",
            "Szczególna forma prawna",
            "Data powstania",
            "Data rozpoczęcia działalności",
        ]

    def translate_column_name(self, row):
        return {
            "NIP": row["nip"],
            "KRS": row["krs"],
            "REGON": row["regon"],
            "Nazwa": row["name"],
            "Adres1": row["address1"],
            "Adres2": row["address2"],
            "Kod pocztowy": row["zip"],
            "Miejscowość": row["city"],
            "Województwo": row["state"],
            "Strona WWW": row["website"],
            "Facebook": row["facebook"],
            "LinkedIn": row["linkedin"],
            "Przedział zatrudnienia": row["employment_range"],
            "Podstawowa forma prawna": row["basic_legal_form"],
            "Szczególna forma prawna": row["specific_legal_form"],
            "Data powstania": row["establishment_date"],
            "Data rozpoczęcia działalności": row["start_date"],
        }

    def get_row(self):
        for row in self.data:
            yield self.translate_column_name(row)
