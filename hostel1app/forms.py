from django import forms
from .models import FeeReceipt

class FeeReceiptForm(forms.ModelForm):
    class Meta:
        model = FeeReceipt
        fields = ['full_name', 'utr_number', 'date', 'hostel_name']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
