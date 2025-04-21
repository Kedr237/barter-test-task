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

        cls.url = reverse('ad_list')

    def test_correct_template_used(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/ad_list.html')

    def test_getting_ad_list(self):
        response = self.client.get(self.url)
        ads = response.context['ads']
        self.assertEqual(len(ads), 2)
        self.assertIn(self.ad1, ads)
        self.assertIn(self.ad2, ads)

    def test_filter_by_title_query(self):
        response = self.client.get(self.url, {'query': 'title1'})
        ads = response.context['ads']
        self.assertEqual(len(ads), 1)
        self.assertEqual(ads[0], self.ad1)

    def test_filter_by_description_query(self):
        response = self.client.get(self.url, {'query': 'description2'})
        ads = response.context['ads']
        self.assertEqual(len(ads), 1)
        self.assertEqual(ads[0], self.ad2)

    def test_filter_by_condition(self):
        url = reverse('ad_list')
        response = self.client.get(self.url, {'condition': 'used'})
        ads = response.context['ads']
        self.assertEqual(len(ads), 1)
        self.assertEqual(ads[0], self.ad2)

    def test_filter_by_category(self):
        response = self.client.get(self.url, {'category': self.category1.id})
        ads = response.context['ads']
        self.assertEqual(len(ads), 1)
        self.assertEqual(ads[0], self.ad1)

    def test_filter_form_in_context(self):
        response = self.client.get(self.url)
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

        cls.username = cls.user1.username
        cls.password = 'testpass1'

        cls.url = reverse('my_ad_list')

    def test_redirect_for_anon_user(self):
        redirect_url = reverse('login')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{redirect_url}?next={self.url}')

    def test_status_code_ok(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/my_ad_list.html')

    def test_user_ads_in_context(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        ads = response.context['ads']
        self.assertEqual(len(ads), 1)
        self.assertIn(self.ad1, ads)
        self.assertNotIn(self.ad2, ads)


class AdDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.username1 = 'username1'
        cls.password1 = 'testpass1'
        cls.username2 = 'username2'
        cls.password2 = 'testpass2'

        cls.user1 = User.objects.create_user(
            username=cls.username1,
            password=cls.password1,
        )
        cls.user2 = User.objects.create_user(
            username=cls.username2,
            password=cls.password2,
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

        cls.url = reverse('ad_detail', kwargs={'id': cls.ad1.id})


    def test_status_code_ok(self):
        self.client.login(username=self.username1, password=self.password1)
        url = reverse('my_ad_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_for_anon_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'title1')
        self.assertNotIn('ad_form', response.context)
        self.assertNotIn('proposal_form', response.context)

    def test_for_owner_user(self):
        self.client.login(username=self.username1, password=self.password1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ad_form', response.context)
        self.assertNotIn('proposal_form', response.context)

    def test_for_other_user(self):
        self.client.login(username=self.username2, password=self.password2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('ad_form', response.context)
        self.assertIn('proposal_form', response.context)

    def test_owner_edit_ad(self):
        self.client.login(username=self.username1, password=self.password1)
        data = {
            'edit_ad': '',
            'title': 'updated title1',
            'description': 'updated description1',
            'category': self.category1.id,
            'condition': Ad.Condition.NEW,
        }
        response = self.client.post(self.url, data)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, data['title'])
        self.assertEqual(self.ad1.description, data['description'])
        self.assertRedirects(response, self.url)

    def test_anon_edit_ad(self):
        data = {
            'edit_ad': '',
            'title': 'updated title1',
            'description': 'updated description1',
            'category': self.category1.id,
            'condition': Ad.Condition.NEW,
        }
        response = self.client.post(self.url, data)
        self.ad1.refresh_from_db()
        self.assertNotEqual(self.ad1.title, data['title'])
        self.assertRedirects(response, self.url)

    def test_other_user_send_proposal(self):
        self.client.login(username=self.username2, password=self.password2)
        data = {
            'exchange_proposal': '',
            'ad_sender': self.ad2.id,
            'comment': 'comment',
            'status': 'pending',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        proposal = ExchangeProposal.objects.first()
        self.assertEqual(proposal.ad_receiver, self.ad1)
        self.assertEqual(proposal.ad_sender, self.ad2)
        self.assertEqual(proposal.ad_sender.user, self.user2)
        self.assertRedirects(response, self.url)
