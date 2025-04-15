from django.contrib import admin

from .models import Ad, Category, ExchangeProposal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    ...


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    ...
