# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import UserManager, TopUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.last_name is '' or self.first_name is '':
            return None
        elif self.middle_name is None or self.middle_name == '':
            return super(CustomUser, self).get_full_name()
        else:
            return "%s %s. %s" % (self.first_name, self.middle_name[0], self.last_name)

    def get_number_of_published_posts(self):
        return self.preaching_set.count()

    objects = UserManager()
    top_user = TopUserManager()