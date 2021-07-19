import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'conf.settings'
django.setup()

import jobs.data  # noqa: E402
from jobs.models import Company, Specialty, Vacancy  # noqa: E402


if __name__ == '__main__':

    for company in jobs.data.companies:

        Company.objects.create(
            name=company['title'],
            location=company['location'],
            logo=company['logo'],
            description=company['description'],
            employee_count=company['employee_count'],
        )

    for specialty in jobs.data.specialties:

        Specialty.objects.create(
            code=specialty['code'],
            title=specialty['title'],
        )

    for job in jobs.data.jobs:

        Vacancy.objects.create(
            title=job['title'],
            specialty=Specialty.objects.get(code=job['specialty']),
            company=Company.objects.get(id=job['company']),
            skills=job['skills'],
            description=job['description'],
            salary_min=job['salary_from'],
            salary_max=job['salary_to'],
            published_at=job['posted'],
        )
