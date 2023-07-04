from datetime import datetime


def get_pca_from_file(row):
    department = row["PKD"][0:2] if row["PKD"] else ""
    return {"section": row["Sekcja PKD"], "group": row["PKD"], "department": department}


def get_phones_from_file(row):
    return list(filter(None, [row["Telefon1"], row["Telefon2"]]))


def get_emails_from_file(row):
    return list(filter(None, [row["Email1"], row["Email2"]]))


def get_company_from_file(row):
    address2 = row["Budynek"]
    if address2 and row["Lokal"]:
        address2 += f"/{row['Lokal']}"

    time_format = "%Y%m%d"
    establishment_date = datetime.strptime(row["Data powstania"], time_format).date()
    start_date = datetime.strptime(
        row["Data rozpoczęcia działalności"], time_format
    ).date()

    return {
        "nip": row["NIP"],
        "krs": row["KRS"],
        "regon": row["REGON"],
        "name": row["Nazwa"],
        "address1": row["Ulica"],
        "address2": address2,
        "zip": row["Kod pocztowy"],
        "city": row["Miejscowość"],
        "state": row["Województwo"],
        "website": row["Strona WWW"],
        "facebook": row.get("Facebook"),
        "linkedin": row["LinkedIn"],
        "employment_range": row["Przedział zatrudniena"],
        "basic_legal_form": row["Podstawowa forma prawna"],
        "specific_legal_form": row["Szczególna forma prawna"],
        "establishment_date": establishment_date,
        "start_date": start_date,
    }


def extract_data_from_file(row):
    return {
        "pca": get_pca_from_file(row),
        "company": get_company_from_file(row),
        "phones": get_phones_from_file(row),
        "emails": get_emails_from_file(row),
    }
