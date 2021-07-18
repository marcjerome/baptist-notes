import sys
sys.path.append("..")
from datetime import date
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from users import models
from django.template.loader import render_to_string
from .views import PreachingList, PreachingDelete, PreachingDetailView, PreachingCreateView
from .models import Preaching, Tag

class HomePageTest(TestCase):
    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, PreachingList)

    def test_homepage_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'preachings/index_preaching_list.html')

    def test_success_status_code_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class CreatePreachingPageTest(TestCase):
    def test_create_url_resolves_to_create_preaching_view(self):
        found = resolve('/note/add/')
        self.assertEqual(found.func.view_class, PreachingCreateView)

    def test_success_status_code_preaching_create_page_user_authenticated(self):
        user = models.CustomUser.objects.create(username='admin')
        user.set_password('admin')
        user.save()

        self.client.login(username='admin', password='admin')
        response = self.client.get('/note/add/')
        self.assertEqual(response.status_code, 200)
    
    def test_redirect_status_code_preaching_create_page_user_unauthenticated(self):
        response = self.client.get('/note/add/')
        self.assertEqual(response.status_code, 302)

    def test_create_preaching_page_returns_correct_html(self):
        user = models.CustomUser.objects.create(username='admin')
        user.set_password('admin')
        user.save()

        self.client.login(username='admin', password='admin')
        response = self.client.get('/note/add/')
        self.assertTemplateUsed(response, 'preachings/preaching_create.html')
    
    def test_create_preaching_page_redirects_to_login_if_unauthenticated(self):
        response = self.client.get('/note/add/', follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_post_create_preaching_valid(self):
        user = models.CustomUser.objects.create(username='admin')
        user.set_password('admin')
        user.save()
        self.client.login(username='admin', password='admin')
        
        data={'title': 'test', 'text': 'test', 'date': date.today(), 'tags': 'test' }
        response = self.client.post('/note/add/', data)
       
        self.assertEqual(response.status_code,302)
        
    def test_post_create_preaching_invalid(self):
        user = models.CustomUser.objects.create(username='admin')
        user.set_password('admin')
        user.save()
        self.client.login(username='admin', password='admin')
        
        data={'title': 'test', 'text': 'test', 'tags': 'test' }
        response = self.client.post('/note/add/', data)
        
        self.assertEqual(response.status_code,200)
        
        # TO DO: FIX THIS TEST
        
        #self.assertContains(response, 'This field is required.', html=False)
    
class DeletePreachingPageTest(TestCase):
    slug = ''
    
    def setUp(self):
        user = models.CustomUser.objects.create(username='admin')
        user.set_password('admin')
        user.save()
        
        self.client.login(username='admin', password='admin')

        data={'title': 'test', 'text': 'test', 'date': date.today(), 'tags': 'test' }
        self.client.post('/note/add/', data)
        
        preaching = Preaching.objects.all().first()
        self.slug = preaching.slug


    def test_delete_url_resolves_to_delete_preaching_view(self):
        found = resolve('/note/delete/{slug}/'.format(slug=self.slug))
        self.assertEqual(found.func.view_class, PreachingDelete)

    def test_delete_preaching_page_returns_correct_html(self):
        response = self.client.get('/note/delete/{slug}/'.format(slug=self.slug))
        self.assertTemplateUsed(response, 'preachings/preaching_confirm_delete.html')

    def test_success_status_code_preaching_delete_page_user_authenticated(self):
        response = self.client.get('/note/delete/{slug}/'.format(slug=self.slug))
        self.assertEqual(response.status_code, 200)
   
    def test_post_delete_preaching_valid(self):     
        response = self.client.post('/note/delete/{slug}/'.format(slug=self.slug))
        self.assertEqual(response.status_code,302)
        
    def test_get_delete_preaching_invalid(self):
        response = self.client.get('/note/delete/{slug}/'.format(slug='random'))
        self.assertEqual(response.status_code,404)

    def test_redirect_status_code_preaching_delete_page_user_unauthenticated(self):
        self.client.logout()
        response = self.client.get('/note/delete/{slug}/'.format(slug=self.slug))
        self.assertEqual(response.status_code, 302)


class PreachingDetailViewTest(TestCase):
    slug = ''
    
    def setUp(self):
        user = models.CustomUser.objects.create(username='admin')
        user.set_password('admin')
        user.save()
        
        self.client.login(username='admin', password='admin')

        data={'title': 'test', 'text': 'test', 'date': date.today(), 'tags': 'test' }
        self.client.post('/note/add/', data)
        
        preaching = Preaching.objects.all().first()
        self.slug = preaching.slug


    def test_preaching_detail_url_resolves_to_preaching_view(self):
        found = resolve('/note/{slug}/'.format(slug=self.slug))
        self.assertEqual(found.func.view_class, PreachingDetailView)

    def test_preaching_detail_page_returns_correct_html(self):
        response = self.client.get('/note/{slug}/'.format(slug=self.slug))
        self.assertTemplateUsed(response, 'preachings/preaching_detail.html')

    def test_success_status_code_preaching_detail_page(self):
        response = self.client.get('/note/{slug}/'.format(slug=self.slug))
        self.assertEqual(response.status_code, 200)

    def test_status_code_for_non_existing_slug(self):
        response = self.client.get('/note/delete/{slug}/'.format(slug='random'))
        self.assertEqual(response.status_code,404)

class TaggedPreachingListViewTest(TestCase):
    pass

    #path('note/update/<slug:slug>/', PreachingUpdate.as_view(), name='preaching_update'),
    #path('<str:tag>/', TaggedPreachingList.as_view(), name='tagged_preaching_list'),
