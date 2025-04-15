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

    def __str__(self):
        return f'Category: "{self.title}"'


class Ad(TimeMixin):

    class Condition(models.TextChoices):
        NEW = 'new', _('New')
        USED = 'used', _('Used')
        REFURBISHED = 'refurbished', _('Refurbished')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = models.TextField(null=True, verbose_name=_('Description'))
    image_url = models.ImageField(null=True, blank=True, verbose_name=_('Image URL (cover)'))
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

    def __str__(self):
        return f'Product: "{self.title}" by {self.user.username}'


class ExchangeProposal(TimeMixin):

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
        CANCELLED = 'cancelled', _('Cancelled')

    ad_sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender',
        verbose_name=_('Sender'),
    )
    ad_receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver',
        verbose_name=_('Receiver'),
    )
    comment = models.TextField(null=True, verbose_name=_('Comment'))
    status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.PENDING,
        verbose_name=_('Status'),
    )

    def __str__(self):
        return f'Exchange from {self.ad_sender.username} to {self.ad_receiver.username} - {self.status}'
