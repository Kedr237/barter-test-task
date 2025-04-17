from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimeMixin(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))

    class Meta:
        abstract = True


class Category(TimeMixin):

    title = models.CharField(max_length=100, verbose_name=_('Category title'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f'{self.title}'


class Ad(TimeMixin):

    class Condition(models.TextChoices):
        NEW = 'new', _('New')
        USED = 'used', _('Used')
        REFURBISHED = 'refurbished', _('Refurbished')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    image = models.ImageField(null=True, blank=True, verbose_name=_('Image URL (cover)'))
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Category'),
    )
    condition = models.CharField(
        max_length=20,
        choices=Condition,
        default=Condition.NEW,
        verbose_name=_('Condition'),
    )

    class Meta:
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')

    def __str__(self):
        return f'"{self.title}" by {self.user.username}'


class ExchangeProposal(TimeMixin):

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
        CANCELLED = 'cancelled', _('Cancelled')

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='sent_proposals',
        verbose_name=_('Sender'),
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='received_proposals',
        verbose_name=_('Receiver'),
    )
    comment = models.TextField(null=True, blank=True, verbose_name=_('Comment'))
    status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.PENDING,
        verbose_name=_('Status'),
    )

    class Meta:
        verbose_name = _('Proposal')
        verbose_name_plural = _('Proposals')

    def __str__(self):
        return f'Exchange from {self.ad_sender.title} to {self.ad_receiver.title} - {self.status}'
