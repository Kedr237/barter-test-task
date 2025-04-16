import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from ads.models import Ad, Category, ExchangeProposal

User = get_user_model()
fake = Faker('ru_RU')


class Command(BaseCommand):

    help = 'Generate mock data.'

    def handle(self, *args, **kwargs):
        TARGET_USERS = 20
        TARGET_CATEGORIES = 10
        TARGET_ADS = 100
        TARGET_PROPOSALS = 20

        need_users = TARGET_USERS - User.objects.count()
        need_categories = TARGET_CATEGORIES - Category.objects.count()
        need_ads = TARGET_ADS - Ad.objects.count()
        need_proposals = TARGET_PROPOSALS - ExchangeProposal.objects.count()

        # users
        if need_users > 0:
            users = list(User.objects.all())
            for _ in range(need_users):
                user = User.objects.create_user(
                    username=fake.user_name(),
                    password=fake.password(length=10, special_chars=True),
                    email=fake.email(),
                )
                users.append(user)
        else:
            users = list(User.objects.all()[:TARGET_USERS])

        # categories
        if need_categories > 0:
            categories = list(Category.objects.all())
            for _ in range(need_categories):
                category = Category.objects.create(
                    title=fake.word().capitalize(),
                )
                categories.append(category)
        else:
            categories = list(Category.objects.all()[:TARGET_CATEGORIES])

        # ads
        if need_ads > 0:
            ads = list(Ad.objects.all())
            conditions = [choice[0] for choice in Ad.Condition.choices]
            for _ in range(need_ads):
                ad = Ad.objects.create(
                    user=random.choice(users),
                    title=fake.sentence(nb_words=3).rstrip('.'),
                    description='\n'.join([fake.text(max_nb_chars=100) for _ in range(3)]),
                    category=random.choice(categories),
                    condition=random.choice(conditions),
                )
                ads.append(ad)
        else:
            ads = list(Ad.objects.all()[:TARGET_ADS])

        # proposals
        if need_proposals > 0:
            statuses = [choice[0] for choice in ExchangeProposal.Status.choices]
            for _ in range(need_proposals):
                ad_sender = random.choice(ads)
                ad_receiver = random.choice([ad for ad in ads if ad != ad_sender])
                ExchangeProposal.objects.create(
                    ad_sender=ad_sender,
                    ad_receiver=ad_receiver,
                    comment='\n'.join([fake.text(max_nb_chars=100) for _ in range(3)]),
                    status=random.choice(statuses),
                )
