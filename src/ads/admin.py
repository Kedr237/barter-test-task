from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Ad, Category, ExchangeProposal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'id',)
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'condition', 'id',)
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('ad_sender', 'ad_receiver', 'short_comment', 'status', 'id',)
    readonly_fields = ('created_at', 'updated_at',)
    
    def short_comment(self, obj: ExchangeProposal):
        comment = obj.comment
        return comment[:20] + '...' if len(comment) > 20 else comment
    short_comment.short_description = _('Comment')
