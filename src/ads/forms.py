from django import forms

from .models import Ad


class CustomClearableFileInput(forms.ClearableFileInput):

    template_name = 'ads/widgets/custom_clearable_file_input.html'


class AdForm(forms.ModelForm):

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
            'image_url': CustomClearableFileInput(attrs={
                'class': 'ad-form__widget ad-form__image',
            }),
            'category': forms.Select(attrs={
                'class': 'ad-form__widget ad-form__category',
            }),
            'condition': forms.Select(attrs={
                'class': 'ad-form__widget ad-form__condition',
            }),
        }

    def clean_image_url(self):
        image = self.cleaned_data.get('image_url')
        image_clear = self.cleaned_data.get('image_url-clear')
        if image_clear:
            return None
        return image
