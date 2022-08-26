# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.test import TestCase
from django.urls import resolve
from .views import UserDetailView, RegisterView, UserUpdate, CustomPasswordChangeView, CustomPasswordChangeDone
from .models import CustomUser

class UserDetailTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(username='admin', email='admin@admin.com')
        user.set_password('admin')
        user.save()
        self.user = user

    def test_user_detail_url_resolves_to_user_detail_view(self):
        found = resolve('/user/{id}/'.format(id=self.user.id))
        self.assertEqual(found.func.view_class, UserDetailView)

    def test_success_status_code(self):
        response = self.client.get('/user/{id}/'.format(id=self.user.id))
        self.assertEqual(response.status_code, 200)

    def test_user_detail_uses_correct_template(self):
        response = self.client.get('/user/{id}/'.format(id=self.user.id))
        self.assertTemplateUsed(response, 'users/user_detail.html')
    
class TestRegisterView(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(username='admin', email='admin@admin.com')
        user.set_password('admin')
        user.save()
        self.user = user

    def test_register_view_uses_correct_html(self):
        response = self.client.get('/accounts/register/')
        self.assertTemplateUsed(response, 'registration/user_create.html' )
    
    def test_success_status_code_register_view(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_url_resolves_to_register_view(self):
        found = resolve('/accounts/register/')
        self.assertEqual(found.func.view_class, RegisterView)

    def test_redirect_to_correct_html_after_success_register(self):
        data = {
            'username':'admin2', 
            'email':'admin2@admin.com',
            'password1': '321Testing',
            'password2': '321Testing',
            'first_name': 'Marc Jerome',
            'middle_name': 'Talla',
            'last_name': 'Tulali'
        }
        response = self.client.post('/accounts/register/',data, follow=True)
        self.assertTemplateUsed(response, 'preachings/index_preaching_list.html')

    def test_redirect_authenticated_user_to_correct_html(self):
        self.client.login(email='admin@admin.com', password='admin')
        response = self.client.get('/accounts/register/', follow=True)
        self.assertTemplateUsed(response, 'preachings/index_preaching_list.html')
    

class UserUpdateTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(username='admin', email='admin@admin.com')
        user.set_password('admin')
        user.save()
        
        user2 = CustomUser.objects.create(username='admin2', email='admin2@admin.com')
        user2.set_password('admin2')
        user2.save()

        self.user = user
        self.user2 = user2 

        self.client.login(email='admin@admin.com', password='admin')

    def test_user_update_test_uses_correct_html(self):
        response = self.client.get('/accounts/update/{id}/'.format(id=self.user.id))
        self.assertTemplateUsed(response, 'users/user_update.html')
        
    def test_success_status_code_user_update_page(self):
        response = self.client.get('/accounts/update/{id}/'.format(id=self.user.id))
        self.assertEqual(response.status_code, 200)

    def test_user_update_url_resolves_to_user_update_view(self):
        found = resolve('/accounts/update/{id}/'.format(id=self.user.id))
        self.assertEqual(found.func.view_class, UserUpdate)
    
    def test_successful_user_update_updates_user(self):
        data = {
            'first_name': 'Marc',
            'last_name': 'Tulali',
            'bio': 'Test',
            'middle_name': 'Talla',
            'username': 'admin'
        }
        self.client.post('/accounts/update/{id}/'.format(id=self.user.id), data,)
        user = CustomUser.objects.get(id=self.user.id)
        self.assertEqual(data['first_name'], user.first_name)
        self.assertEqual(data['last_name'], user.last_name)
        self.assertEqual(data['middle_name'],user.middle_name)
        self.assertEqual(data['username'], user.username)
        self.assertEqual(data['bio'], user.bio)
        
        
    def test_redirect_to_correct_html_after_successful_update(self):
        data = {
            'first_name': 'Marc',
            'last_name': 'Tulali',
            'bio': 'Test',
            'middle_name': 'Talla',
            'username': 'admin'
        }
        response = self.client.post('/accounts/update/{id}/'.format(id=self.user.id), data, follow=True)
        self.assertTemplateUsed(response, 'users/user_detail.html')

    def unauthorized_user_redirects_to_correct_html(self):
        response = self.client.get('/accounts/update/{id}/'.format(id=self.user2.id))
        self.assertTemplateUsed(response, 'preachings/index_preaching_list.html')
        

    def test_redirect_authenticated_user_to_correct_html_in_user_update(self):
        self.client.logout()
        response = self.client.get('/accounts/update/{id}/'.format(id=self.user.id), follow=True)
        self.assertTemplateUsed(response, 'preachings/index_preaching_list.html')

class CustomPasswordChangeTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(username='admin', email='admin@admin.com')
        user.set_password('admin')
        user.save()

        self.client.login(email='admin@admin.com', password='admin')

    def test_success_status_code_custom_password_change_view(self):
        response = self.client.get('/accounts/password_change/')
        self.assertEqual(response.status_code, 200)

    def test_custom_password_change_uses_correct_html(self):
        response = self.client.get('/accounts/password_change/')
        self.assertTemplateUsed(response, 'registration/password_change.html')

    def test_custom_password_change_resolves_to_correct_view(self):
        found = resolve('/accounts/password_change/')
        self.assertEqual(found.func.view_class, CustomPasswordChangeView)

    def test_successful_change_password_redirects_to_correct_html(self):
        data = {
            'old_password':'admin',
            'new_password1': 'Testing321',
            'new_password2': 'Testing321'
        }
        response = self.client.post('/accounts/password_change/', data, follow=True)
        self.assertTemplateUsed(response, 'registration/password_change_success.html')

    def test_unauthenticated_user_redirect_to_correct_html(self):
        self.client.logout()
        data = {
            'old_password':'admin',
            'new_password1': 'Testing321',
            'new_password2': 'Testing321'
        }
        response = self.client.post('/accounts/password_change/', data, follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

        
class CustomPasswordChangeDoneTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(username='admin', email='admin@admin.com')
        user.set_password('admin')
        user.save()

        data = {
            'old_password':'admin',
            'new_password1': 'Testing321',
            'new_password2': 'Testing321'
        }
        self.data = data
        self.client.login(email='admin@admin.com', password='admin')

    def test_success_status_code_custom_password_change_done_view(self):
        response = self.client.get('/accounts/password_change_success/')
        self.assertEqual(response.status_code, 200)
        
    def test_custom_password_change_done_uses_correct_html(self):
        response = self.client.get('/accounts/password_change_success/')
        self.assertTemplateUsed(response, 'registration/password_change_success.html')

    def test_custom_password_change_done_resolves_to_correct_view(self):
        found = resolve('/accounts/password_change_success/')
        self.assertEqual(found.func.view_class, CustomPasswordChangeDone)

    def test_unauthenticated_user_redirect_to_correct_html(self):
        self.client.logout()

        response = self.client.get('/accounts/password_change_success/', follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')
