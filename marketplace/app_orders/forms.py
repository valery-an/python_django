from django import forms
from app_orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('city', 'address', 'delivery', 'payment', 'comment')
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-input', 'data-validate': 'require'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'data-validate': 'require'}),
            'delivery': forms.RadioSelect,
            'payment': forms.RadioSelect,
            'comment': forms.Textarea(attrs={'class': 'form-textarea'})
        }
