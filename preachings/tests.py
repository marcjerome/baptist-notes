import sys
sys.path.append("..")
from datetime import date
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from users import models
from django.template.loader import render_to_string
from .views import PreachingList, PreachingDelete, PreachingDetailView, PreachingCreateView, TaggedPreachingList, PreachingUpdate
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

    def setUp(self):
        user = models.CustomUser.objects.create(username='admin')
        user.set_password('admin')
        user.save()
 
        self.client.login(username='admin', password='admin')
        
        tag = Tag(title='thisisatest')
        tag.save()

        preaching = Preaching.objects.create(user=user, title='testtitlee', text='test', date=date.today(), privacy=False)
       
        preaching.tags.add(tag)

        self.tag_title = tag.title

    def test_success_status_code_tagged_preaching_list_page(self):
        response = self.client.get('/tag/{tag}/'.format(tag=self.tag_title))
        self.assertEqual(response.status_code, 200)

    def test_tagged_preaching_list_page_returns_correct_html(self):
        response = self.client.get('/tag/{tag}/'.format(tag=self.tag_title))
        self.assertTemplateUsed(response, 'preachings/index_preaching_list.html')


    def test_tagged_preaching_url_resolves_to_tagged_preaching_list_view(self):
        found = resolve('/tag/{tag}/'.format(tag=self.tag_title))
        self.assertEqual(found.func.view_class, TaggedPreachingList)



class PreachingUpdateViewTest(TestCase):
    def setUp(self):
        user = models.CustomUser.objects.create(username='admin')
        user.set_password('admin')
        user.save()

        user2 = models.CustomUser.objects.create(username='admin2')
        user2.set_password('admin2')
        user2.save()

        self.client.login(username='admin', password='admin')

        tag = Tag(title='thisisatest')
        tag.save()

        preaching = Preaching.objects.create(user=user, title='testtitlee', text='test', date=date.today(), privacy=False)
       
        preaching.tags.add(tag)

        self.slug = preaching.slug


        preaching2 = Preaching.objects.create(user=user, title='testtitlee2', text='test2', date=date.today(), privacy=False)
       
        preaching2.tags.add(tag)

        self.slug2 = preaching2.slug

    def test_success_status_code_preaching_update_page(self):
        response = self.client.get('/note/update/{slug}/'.format(slug=self.slug))
        self.assertEqual(response.status_code, 200)

    def test_preaching_update_page_returns_correct_html(self):
        response = self.client.get('/note/update/{slug}/'.format(slug=self.slug))
        self.assertTemplateUsed(response, 'preachings/preaching_update.html')

    def test_preaching_update_page_url_resolves_to_preaching_update_view(self):
        found = resolve('/note/update/{slug}/'.format(slug=self.slug))
        self.assertEqual(found.func.view_class, PreachingUpdate)

    def test_redirect_status_code_preaching_delete_page_user_unauthenticated(self):
        self.client.logout()
        response = self.client.get('/note/update/{slug}/'.format(slug=self.slug))
        self.assertEqual(response.status_code, 302)


    def test_cant_update_preaching__of_other_publishers(self):
        self.client.login(username='admin2', password='admin2')
        data = {'title': 'update', 'text': 'test', 'date': date.today(), 'tags': 'test' }
        self.client.post('/note/update/{slug}/'.format(slug=self.slug), data)
        preaching = Preaching.objects.filter(title='update').first()
        self.assertIsNone(preaching)

    def test_can_update_own_published_preaching(self):
        data = {'title': 'update', 'text': 'test', 'date': date.today(), 'tags': 'test' }
        self.client.post('/note/update/{slug}/'.format(slug=self.slug2), data)
        preaching = Preaching.objects.filter(title='update').first()
        self.assertIsNotNone(preaching)
    
    def test_redirect_to_preaching_detail_after_preaching_update(self):
        data = {'title': 'update', 'text': 'test', 'date': date.today(), 'tags': 'test' }
        response = self.client.post('/note/update/{slug}/'.format(slug=self.slug2), data, follow=True)
        self.assertTemplateUsed(response, 'preachings/preaching_detail.html')


