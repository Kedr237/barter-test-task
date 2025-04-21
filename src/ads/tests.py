from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Ad, Category, ExchangeProposal

User = get_user_model()


class AdListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass1',
        )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass2',
        )

        cls.category1 = Category.objects.create(title='category')
        cls.category2 = Category.objects.create(title='category')

        cls.ad1 = Ad.objects.create(
            user=cls.user1,
            title='title1 title1',
            description='description1 description1',
            category=cls.category1,
            condition=Ad.Condition.NEW,
        )
        cls.ad2 = Ad.objects.create(
            user=cls.user2,
            title='title2 title2',
            description='description2 description2',
            category=cls.category2,
            condition=Ad.Condition.USED,
        )

    def test_correct_template_used(self):
        url = reverse('ad_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/ad_list.html')

    def test_getting_ad_list(self):
        url = reverse('ad_list')
        response = self.client.get(url)
        ads = response.context['ads']
        self.assertEqual(len(ads), 2)
        self.assertIn(self.ad1, ads)
        self.assertIn(self.ad2, ads)

    def test_filter_by_title_query(self):
        url = reverse('ad_list')
        response = self.client.get(url, {'query': 'title1'})
        ads = response.context['ads']
        self.assertEqual(len(ads), 1)
        self.assertEqual(ads[0], self.ad1)

    def test_filter_by_description_query(self):
        url = reverse('ad_list')
        response = self.client.get(url, {'query': 'description2'})
        ads = response.context['ads']
        self.assertEqual(len(ads), 1)
        self.assertEqual(ads[0], self.ad2)

    def test_filter_by_condition(self):
        url = reverse('ad_list')
        response = self.client.get(url, {'condition': 'used'})
        ads = response.context['ads']
        self.assertEqual(len(ads), 1)
        self.assertEqual(ads[0], self.ad2)

    def test_filter_by_category(self):
        url = reverse('ad_list')
        response = self.client.get(url, {'category': self.category1.id})
        ads = response.context['ads']
        self.assertEqual(len(ads), 1)
        self.assertEqual(ads[0], self.ad1)

    def test_filter_form_in_context(self):
        url = reverse('ad_list')
        response = self.client.get(url)
        self.assertIn('filter_form', response.context)



class MyAdListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass1',
        )
        cls.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass2',
        )

        cls.category1 = Category.objects.create(title='category')
        cls.category2 = Category.objects.create(title='category')

        cls.ad1 = Ad.objects.create(
            user=cls.user1,
            title='title1 title1',
            description='description1 description1',
            category=cls.category1,
            condition=Ad.Condition.NEW,
        )
        cls.ad2 = Ad.objects.create(
            user=cls.user2,
            title='title2 title2',
            description='description2 description2',
            category=cls.category2,
            condition=Ad.Condition.USED,
        )

    def setUp(self):
        self.username = self.user1.username
        self.password = 'testpass1'

    def test_redirect_for_not_auth_user(self):
        url = reverse('my_ad_list')
        redirect_url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{redirect_url}?next={url}')

    def test_status_code_ok(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('my_ad_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('my_ad_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/my_ad_list.html')

    def test_user_ads_in_context(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('my_ad_list')
        response = self.client.get(url)
        ads = response.context['ads']
        self.assertEqual(len(ads), 1)
        self.assertIn(self.ad1, ads)
        self.assertNotIn(self.ad2, ads)
