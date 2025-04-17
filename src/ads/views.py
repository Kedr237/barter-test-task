from django.views.generic import ListView

from .models import Ad


class AdListView(ListView):
    paginate_by = 20
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']
