from django import forms

from .models import Ad, ExchangeProposal


class CustomClearableFileInput(forms.ClearableFileInput):

    template_name = 'ads/widgets/custom_clearable_file_input.html'


class AdForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = ('title', 'description', 'image', 'category', 'condition')
        labels = {
            'image': 'Изображение',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'ad-form__widget ad-form__title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'ad-form__widget ad-form__description',
            }),
            'image': CustomClearableFileInput(attrs={
                'class': 'ad-form__widget ad-form__image',
            }),
            'category': forms.Select(attrs={
                'class': 'ad-form__widget ad-form__category',
            }),
            'condition': forms.Select(attrs={
                'class': 'ad-form__widget ad-form__condition',
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        image_clear = self.cleaned_data.get('image-clear')
        if image_clear:
            return None
        return image


class ExchangeProposalForm(forms.ModelForm):

    class Meta:
        model = ExchangeProposal
        fields = ('ad_sender', 'comment')
        labels = {
            'ad_sender': 'Я предлагаю',
        }
        widgets = {
            'ad_sender': forms.Select(attrs={
                'class': 'proposal-form__widget proposal-form__select',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'proposal-form__widget proposal-form__comment',
            })
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            queryset = Ad.objects.filter(user=user)
            self.fields['ad_sender'].queryset = queryset
            self.fields['ad_sender'].label_from_instance = lambda obj: obj.title
