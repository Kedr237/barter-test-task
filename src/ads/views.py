from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View

from .forms import AdFilterForm, AdForm, ExchangeProposalForm, ProposalFilterForm
from .models import Ad, ExchangeProposal


class AdListView(ListView):

    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = AdFilterForm(self.request.GET)

        if self.form.is_valid():
            query = self.form.cleaned_data.get('query')
            category = self.form.cleaned_data.get('category')
            condition = self.form.cleaned_data.get('condition')

            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | \
                    Q(description__icontains=query)
                )
            if category:
                queryset = queryset.filter(category=category)
            if condition:
                queryset = queryset.filter(condition=condition)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = getattr(self, 'form', AdFilterForm())
        return context


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
                context['proposals_for_me'] = ExchangeProposal.objects.filter(ad_receiver__user=user, ad_receiver=ad)
            if user != ad.user:
                context['proposal_form'] = ExchangeProposalForm(user=user, ad_receiver=ad)
                context['my_proposals'] = ExchangeProposal.objects.filter(ad_sender__user=user, ad_receiver=ad)
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        ad: Ad = self.object
        user = request.user

        # Processing the edit form.
        if 'edit_ad' in request.POST:
            if not user.is_authenticated or user != ad.user:
                return redirect(request.path)

            form = AdForm(request.POST, request.FILES, instance=ad)
            if form.is_valid():
                form.save()
                return redirect(request.path)

            context = self.get_context_data()
            context['ad_form'] = form
            return self.render_to_response(context)
        
        # Processing the exchange form.
        elif 'exchange_proposal' in request.POST:
            if not user.is_authenticated or user == ad.user:
                return redirect(request.path)
            
            form = ExchangeProposalForm(request.POST, user=user)
            if form.is_valid():
                proposal = form.save(commit=False)
                proposal.ad_receiver = ad
                proposal.save()
                return redirect(request.path)

            context = self.get_context_data()
            context['proposal_form'] = form
            return self.render_to_response(context)

        return redirect(request.path)


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


class ProposalDeleteView(View, LoginRequiredMixin):

    def post(self, request: HttpRequest, id: int):
        proposal = get_object_or_404(ExchangeProposal, id=id)
        if proposal.ad_sender.user == request.user:
            proposal.delete()

        referer = request.META.get('HTTP_REFERER')

        if referer and 'proposals/edit' not in referer:
            return redirect(referer)

        return redirect('my_proposals')


class MyProposalsView(ListView, LoginRequiredMixin):

    model = ExchangeProposal
    template_name = 'ads/my_proposals.html'
    context_object_name = 'proposals'
    paginate_by = 20

    def get_queryset(self):
        queryset = ExchangeProposal.objects.filter(
            ad_sender__user=self.request.user,
        ).order_by('-created_at')
        self.form = ProposalFilterForm(self.request.GET)

        if self.form.is_valid():
            user_query = self.form.cleaned_data.get('user_query')
            status = self.form.cleaned_data.get('status')

            if user_query:
                queryset = queryset.filter(
                    Q(ad_receiver__user__username__icontains=user_query)
                )
            if status:
                queryset = queryset.filter(status=status)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = getattr(self, 'form', ProposalFilterForm())
        return context


class ProposalsForMeView(ListView, LoginRequiredMixin):

    model = ExchangeProposal
    template_name = 'ads/proposals_for_me.html'
    context_object_name = 'proposals'
    paginate_by = 20

    def get_queryset(self):
        queryset = ExchangeProposal.objects.filter(
            ad_receiver__user__username=self.request.user,
        ).order_by('-created_at')
        self.form = ProposalFilterForm(self.request.GET)

        if self.form.is_valid():
            user_query = self.form.cleaned_data.get('user_query')
            status = self.form.cleaned_data.get('status')

            if user_query:
                queryset = queryset.filter(
                    Q(ad_sender__user__username__icontains=user_query)
                )
            if status:
                queryset = queryset.filter(status=status)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = getattr(self, 'form', ProposalFilterForm())
        return context


class EditProposalView(DetailView, LoginRequiredMixin):

    model = ExchangeProposal
    template_name = 'ads/edit_proposal.html'
    context_object_name = 'proposal'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposal: ExchangeProposal = self.object
        user = self.request.user
        if user.is_authenticated and user == proposal.ad_sender.user:
            context['proposal_form'] = ExchangeProposalForm(user=user, instance=proposal)
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        proposal: ExchangeProposal = self.object
        user = request.user

        if not user.is_authenticated or user != proposal.ad_sender.user:
            return redirect(request.path)
        
        form = ExchangeProposalForm(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            return redirect(request.path)
        
        context = self.get_context_data()
        context['proposal_form'] = form
        return self.render_to_response(context)
