from django import forms

from apps.reports.models import Report

__all__ = (
    'ReportForm',
)


class ReportForm(forms.ModelForm):
    """Form for creating report in views"""

    class Meta:
        model = Report
        fields = ('reason',)
