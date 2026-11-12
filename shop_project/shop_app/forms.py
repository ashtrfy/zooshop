from django import forms

from .models import (
    Age, AnimalType, Category, Manufacturer, PaymentMethod, PickupPoint, Review, Size,
)


class FilterForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.HiddenInput)
    type = forms.ModelChoiceField(
        queryset=AnimalType.objects.all(), required=False, widget=forms.HiddenInput
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )
    age = forms.ModelMultipleChoiceField(
        queryset=Age.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )
    size = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )
    manufacturer = forms.ModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )
    price_min = forms.DecimalField(
        required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'От...'})
    )
    price_max = forms.DecimalField(
        required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'До...'})
    )
    rating = forms.ChoiceField(
        required=False,
        choices=[('5', 'от 5 звезд'), ('4', 'от 4 звезд'), ('3', 'от 3 звезд')],
        widget=forms.RadioSelect,
    )


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')])

    class Meta:
        model = Review
        fields = ['rating', 'text']


class OrderForm(forms.Form):
    pickup_point = forms.ModelChoiceField(queryset=PickupPoint.objects.all(), label='Пункт выдачи')
    payment_method = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), label='Способ оплаты')
