from django import forms

class ResumeUploadForm(forms.Form):
    resume = forms.FileField(
        label = "Upload Resume (PDF or DOCX Only)",
        widget = forms.FileInput(attrs={
            "accept": ".pdf, .docx",
            "class": "form-control"
        })
    )

    target_role = forms.CharField(
        max_length = 200,
        label = "Target Job Role",
        widget = forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g., Software Engineer, Data Analyst"
        })
    )