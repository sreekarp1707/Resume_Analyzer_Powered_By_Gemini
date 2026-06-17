from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import ResumeUploadForm
from .models import ResumeAnalysis

from .utils.file_reader import extract_text
from .utils.gemini_helper import analyze_resume
from .utils.pdf_report import generate_pdf_report


@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)

        if form.is_valid():
            resume_file = request.FILES['resume']
            target_role = form.cleaned_data['target_role']

            resume_text = extract_text(resume_file)

            resume_keywords = [
                "education",
                "experience",
                "skills",
                "projects",
                "certifications",
                "summary"
            ]

            matches = sum(
                1 for keyword in resume_keywords
                if keyword in resume_text.lower()
            )

            if matches < 2:
                form.add_error(
                    'resume',
                    'This does not appear to be a valid resume PDF.'
                )

                return render(
                    request,
                    'analyzer/dashboard.html',
                    {
                        'form': form
                    }
                )

            result = analyze_resume(
                resume_text,
                target_role
            )

            analysis = ResumeAnalysis.objects.create(
                user=request.user,
                resume_file=resume_file,
                target_role=target_role,
                ats_score=result['ats_score'],
                matched_keywords=result['matched_keywords'],
                missing_keywords=result['missing_keywords'],
                suggestions=result['suggestions']
            )

            return redirect('result', pk=analysis.pk)

    else:
        form = ResumeUploadForm()

    return render(
        request,
        'analyzer/dashboard.html',
        {
            'form': form
        }
    )

@login_required
def result(request, pk):
    analysis = get_object_or_404(
        ResumeAnalysis,
        pk=pk,
        user=request.user
    )

    return render(
        request,
        'analyzer/result.html',
        {
            'analysis': analysis
        }
    )


@login_required
def history(request):
    analyses = ResumeAnalysis.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'analyzer/history.html',
        {
            'analyses': analyses
        }
    )


@login_required
def download_report(request, pk):
    analysis = get_object_or_404(
        ResumeAnalysis,
        pk=pk,
        user=request.user
    )

    pdf = generate_pdf_report(analysis)

    response = HttpResponse(
        pdf,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="resume_analysis_{pk}.pdf"'
    )

    return response

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return redirect('login')