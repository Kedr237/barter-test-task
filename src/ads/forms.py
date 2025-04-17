from django import forms

from .models import Ad


class AdCreateForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('title', 'description', 'image_url', 'category', 'condition')
        labels = {
            'image_url': 'Изображение',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'ad-form__widget ad-form__title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'ad-form__widget ad-form__description',
            }),
            'image_url': forms.ClearableFileInput(attrs={
                'class': 'ad-form__widget ad-form__image',
            }),
            'category': forms.Select(attrs={
                'class': 'ad-form__widget ad-form__category',
            }),
            'condition': forms.Select(attrs={
                'class': 'ad-form__widget ad-form__condition',
            }),
        }
