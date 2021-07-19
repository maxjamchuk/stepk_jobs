from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import Http404, HttpRequest
from django.shortcuts import render

from jobs.models import Company, Specialty, Vacancy


def main_view(request: HttpRequest):

    specialties = Specialty.objects.annotate(vacancy_count=Count('vacancies'))
    companies = Company.objects.annotate(vacancy_count=Count('vacancies'))

    return render(
        request,
        'jobs/index.html',
        context={'specialties': specialties, 'companies': companies},
    )


def vacancies_view(request: HttpRequest):

    jobs = Vacancy.objects.all().select_related('company')
    jobs_count = jobs.count()

    return render(
        request,
        'jobs/vacancies.html',
        context={'jobs_count': jobs_count, 'jobs': jobs, 'title': 'Все вакансии'},
    )


def vacancies_cat_view(request: HttpRequest, category: str):

    try:
        specialty = Specialty.objects.get(code=category)
    except ObjectDoesNotExist:
        raise Http404

    jobs = Vacancy.objects.filter(specialty_id=specialty.id).all().select_related('company')
    jobs_count = jobs.count()

    return render(
        request,
        'jobs/vacancies.html',
        context={'jobs_count': jobs_count, 'jobs': jobs, 'title': specialty.title},
    )


def vacancy_view(request: HttpRequest, vacancy_id: int):

    try:
        job = Vacancy.objects.get(id=vacancy_id)
    except ObjectDoesNotExist:
        raise Http404

    return render(
        request,
        'jobs/vacancy.html',
        context={'job': job},
    )


def companies_view(request: HttpRequest, company_id: int):

    try:
        company = Company.objects.get(id=company_id)
    except ObjectDoesNotExist:
        raise Http404

    jobs = Vacancy.objects.filter(company_id=company.id).all()
    jobs_count = jobs.count()

    return render(
        request,
        'jobs/company.html',
        context={'jobs_count': jobs_count, 'jobs': jobs, 'title': company.name},
    )
