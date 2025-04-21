from django import forms

from .models import Ad, ExchangeProposal, Category


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
        fields = ('ad_sender', 'comment', 'status')
        labels = {
            'ad_sender': 'Я предлагаю',
        }
        widgets = {
            'ad_sender': forms.Select(attrs={
                'class': 'proposal-form__widget proposal-form__select',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'proposal-form__widget proposal-form__comment',
            }),
            'status': forms.Select(attrs={
                'class': 'proposal-form__widget proposal-form__select',
            }),
        }

    def __init__(self, *args, user=None, ad_receiver=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            user_ads = Ad.objects.filter(user=user)

            if ad_receiver:
                proposed_ad_ids = ExchangeProposal.objects.filter(
                    ad_receiver=ad_receiver,
                    ad_sender__in=user_ads,
                ).values_list('ad_sender_id', flat=True)
                user_ads = user_ads.exclude(id__in=proposed_ad_ids)

            self.fields['ad_sender'].queryset = user_ads
            self.fields['ad_sender'].label_from_instance = lambda obj: obj.title


class AdFilterForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Поиск',
                widget=forms.TextInput(attrs={
            'class': 'filter-form__widget filter-form__query',
        }),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Категория',
        empty_label='Любая',
        widget=forms.Select(attrs={
            'class': 'filter-form__widget filter-form__category',
        }),
    )
    condition = forms.ChoiceField(
        choices=[('', 'Любое')] + list(Ad.Condition.choices),
        required=False,
        label='Состояние',
        widget=forms.Select(attrs={
            'class': 'filter-form__widget filter-form__condition',
        }),
    )


class ProposalFilterForm(forms.Form):
    user_query = forms.CharField(
        required=False,
        label='Пользователь',
                widget=forms.TextInput(attrs={
            'class': 'filter-form__widget filter-form__user-query',
        }),
    )
    status = forms.ChoiceField(
        choices=[('', 'Любой')] + list(ExchangeProposal.Status.choices),
        required=False,
        label='Статус',
        widget=forms.Select(attrs={
            'class': 'filter-form__widget filter-form__status',
        }),
    )
