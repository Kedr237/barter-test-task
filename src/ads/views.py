from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View

from .forms import AdForm, ExchangeProposalForm
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
        user = self.request.user
        if user.is_authenticated:
            if user == ad.user:
                context['ad_form'] = AdForm(instance=ad)
            if user != ad.user:
                context['exchange_form'] = ExchangeProposalForm(user=user)
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        ad: Ad = self.object
        user = request.user

        # Processing the edit form.
        if 'edit_ad' in request.POST:
            if not user.is_authenticated or user != ad.user:
                return redirect('ad_detail', id=ad.id)

            form = AdForm(request.POST, request.FILES, instance=ad)
            if form.is_valid():
                form.save()
                return redirect('ad_detail', id=ad.id)

            context = self.get_context_data()
            context['ad_form'] = form
            return self.render_to_response(context)
        
        # Processing the exchange form.
        elif 'exchange_proposal' in request.POST:
            if not user.is_authenticated or user == ad.user:
                return redirect('ad_detail', id=ad.id)
            
            form = ExchangeProposalForm(request.POST, user=user)
            if form.is_valid():
                proposal = form.save(commit=False)
                proposal.ad_receiver = ad
                proposal.save()
                return redirect('ad_detail', id=ad.id)

            context = self.get_context_data()
            context['exchange_form'] = form
            return self.render_to_response(context)

        return redirect('ad_detail', id=ad.id)


class AdCreateView(CreateView, LoginRequiredMixin):

    model = Ad
    template_name = 'ads/ad_create.html'
    form_class = AdForm
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdDeleteView(View, LoginRequiredMixin):

    def post(self, request: HttpRequest, id: int):
        ad = get_object_or_404(Ad, id=id)
        if ad.user == request.user:
            ad.delete()
        return redirect('my_ad_list')
