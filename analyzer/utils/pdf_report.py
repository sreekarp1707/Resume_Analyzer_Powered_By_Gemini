from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.units import inch

import io


def generate_pdf_report(analysis):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Resume Analysis Report",
            styles['Title']
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            f"<b>Target Role:</b> {analysis.target_role}",
            styles['Normal']
        )
    )

    story.append(
        Paragraph(
            f"<b>ATS Score:</b> {analysis.ats_score}%",
            styles['Normal']
        )
    )

    story.append(
        Paragraph(
            f"<b>Date:</b> {analysis.created_at.strftime('%d %B %Y %I:%M %p')}",
            styles['Normal']
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            "<b>Matched Keywords</b>",
            styles['Heading2']
        )
    )

    story.append(
        Paragraph(
            ", ".join(analysis.matched_keywords)
            if analysis.matched_keywords else "None",
            styles['Normal']
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Missing Keywords</b>",
            styles['Heading2']
        )
    )

    story.append(
        Paragraph(
            ", ".join(analysis.missing_keywords)
            if analysis.missing_keywords else "None",
            styles['Normal']
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Suggestions</b>",
            styles['Heading2']
        )
    )

    story.append(
        Paragraph(
            analysis.suggestions.replace('\n', '<br/>'),
            styles['Normal']
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer