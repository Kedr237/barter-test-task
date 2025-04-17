from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import AdForm
from .models import Ad


class AdListView(ListView):

    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']
    paginate_by = 20


class MyAdListView(ListView, LoginRequiredMixin):

    model = Ad
    template_name = 'ads/my_ad_list.html'
    context_object_name = 'ads'
    paginate_by = 20

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user).order_by('-created_at')


class AdDetail(DetailView):

    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad: Ad = self.get_object()
        if self.request.user == ad.user:
            context['form'] = AdForm(instance=ad)
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user:
            return redirect('ad_detail', id=self.object.id)

        form = AdForm(request.POST, request.FILES, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', id=self.object.id)
        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)


class AdCreateView(CreateView, LoginRequiredMixin):

    model = Ad
    template_name = 'ads/ad_create.html'
    form_class = AdForm
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
