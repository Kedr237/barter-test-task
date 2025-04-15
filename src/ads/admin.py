from django.contrib import admin

from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    ...


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    ...
