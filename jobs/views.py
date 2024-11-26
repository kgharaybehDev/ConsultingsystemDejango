from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from candidates.models import Candidate
from .forms import JobOpportunityForm
from .models import JobOpportunity


def job_opportunity_list(request):
    # Fetch all job opportunities
    job_opportunities = JobOpportunity.objects.all()

    # Sorting logic
    sort_by = request.GET.get("sort", "created_at")  # Default sort by created_at
    order = request.GET.get("order", "asc")  # Default order is ascending
    order_prefix = "" if order == "asc" else "-"
    job_opportunities = job_opportunities.order_by(f"{order_prefix}{sort_by}")

    # Pagination logic
    per_page = int(request.GET.get("per_page", 10))  # Default 10 items per page
    paginator = Paginator(job_opportunities, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "job_opportunities": page_obj,
        "sort_by": sort_by,
        "order": order,
        "per_page": per_page,
    }
    return render(request, 'jobs/job_opportunity_list.html', context)

@login_required
def job_opportunity_create(request):
    if request.method == 'POST':
        form = JobOpportunityForm(request.POST)
        if form.is_valid():
            job_opportunity = form.save()
            messages.success(request, 'Job Opportunity created successfully.')
            return redirect('jobs:job_opportunity_detail', pk=job_opportunity.pk)
    else:
        form = JobOpportunityForm()
    return render(request, 'jobs/job_opportunity_form.html', {'form': form})

@login_required
def job_opportunity_detail(request, pk):
    job_opportunity = get_object_or_404(JobOpportunity, pk=pk)
    assigned_candidates = job_opportunity.candidates.all()
    return render(request, 'jobs/job_opportunity_detail.html', {
        'job_opportunity': job_opportunity,
        'assigned_candidates': assigned_candidates,
    })

@login_required
def job_opportunity_edit(request, pk):
    job_opportunity = get_object_or_404(JobOpportunity, pk=pk)
    if request.method == 'POST':
        form = JobOpportunityForm(request.POST, instance=job_opportunity)
        if form.is_valid():
            job_opportunity = form.save()
            messages.success(request, 'Job Opportunity updated successfully.')
            return redirect('jobs:job_opportunity_detail', pk=job_opportunity.pk)
    else:
        form = JobOpportunityForm(instance=job_opportunity)
    return render(request, 'jobs/job_opportunity_form.html', {'form': form})



@login_required
def job_opportunity_compatible_candidates(request, pk):
    job_opportunity = get_object_or_404(JobOpportunity, pk=pk)

    # Exclude candidates already associated with any job opportunity
    candidates = Candidate.objects.filter(job_opportunities__isnull=True)

    # Filter based on gender
    if job_opportunity.gender != 'Any':
        candidates = candidates.filter(gender=job_opportunity.gender)

    # Filter based on age
    today = date.today()
    min_birth_date = today - relativedelta(years=job_opportunity.maximum_age)
    max_birth_date = today - relativedelta(years=job_opportunity.minimum_age)
    candidates = candidates.filter(birthday__range=(min_birth_date, max_birth_date))

    # Filter based on nationality
    candidates = candidates.filter(nationality__in=job_opportunity.nationalities.all())

    # Filter based on accepted degrees and fields of study
    candidates = candidates.filter(
        educations__degree__in=job_opportunity.accepted_degrees.all(),
        educations__field_of_study__in=job_opportunity.fields_of_study.all()
    ).distinct()

    # Filter based on minimum years of experience
    compatible_candidates = [
        candidate for candidate in candidates if candidate.get_total_experience_years() >= job_opportunity.minimum_years_of_experience
    ]

    # Sorting logic
    sort_by = request.GET.get("sort", "full_name")
    order = request.GET.get("order", "asc")
    reverse_order = order == "desc"

    if sort_by == "full_name":
        compatible_candidates.sort(key=lambda x: x.full_name.lower(), reverse=reverse_order)
    elif sort_by == "email":
        compatible_candidates.sort(key=lambda x: x.email.lower(), reverse=reverse_order)
    elif sort_by == "total_experience":
        compatible_candidates.sort(key=lambda x: x.get_total_experience_years(), reverse=reverse_order)
    elif sort_by == "age":
        compatible_candidates.sort(key=lambda x: x.age_in_years or 0, reverse=reverse_order)

    # Pagination logic
    per_page = int(request.GET.get("per_page", 10))  # Default 10 items per page
    paginator = Paginator(compatible_candidates, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "job_opportunity": job_opportunity,
        "candidates": page_obj,
        "sort_by": sort_by,
        "order": order,
        "per_page": per_page,
    }
    return render(request, 'jobs/job_opportunity_compatible_candidates.html', context)


@login_required
def job_opportunity_add_candidate(request, job_id, candidate_id):
    job_opportunity = get_object_or_404(JobOpportunity, pk=job_id)
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    # Ensure candidate is not already associated with a job opportunity
    if candidate.job_opportunities.exists():
        messages.error(request, 'Candidate is already assigned to a job opportunity.')
    else:
        job_opportunity.candidates.add(candidate)
        messages.success(request, f'Candidate {candidate.full_name} added to job opportunity.')
    return redirect('jobs:job_opportunity_compatible_candidates', pk=job_opportunity.pk)


def job_opportunity_remove_candidate(request, job_id, candidate_id):
    job_opportunity = get_object_or_404(JobOpportunity, pk=job_id)

    candidate = get_object_or_404(Candidate, pk=candidate_id)
    if candidate.job_opportunities.exists():
        print("Job with candidate", job_opportunity)
        job_opportunity.candidates.remove(candidate)
        messages.success(request, f'Candidate {candidate.full_name} removed from job opportunity.')
    else:
        messages.error(request, 'Candidate is not assigned to this job opportunity.')
    return redirect('jobs:job_opportunity_detail', pk =job_opportunity.pk)


def job_opportunity_candidates(request, pk):
    job_opportunity = get_object_or_404(JobOpportunity, pk=pk)
    candidates = job_opportunity.candidates.all()
    return render(request, 'jobs/job_opportunity_candidates.html', {'job_opportunity': job_opportunity, 'candidates': candidates})