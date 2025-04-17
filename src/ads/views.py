from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse_lazy

from .models import Ad
from .forms import AdCreateForm


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']
    paginate_by = 20


class AdDetail(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'
    pk_url_kwarg = 'id'


class AdCreateView(CreateView):
    model = Ad
    template_name = 'ads/ad_create.html'
    form_class = AdCreateForm
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
