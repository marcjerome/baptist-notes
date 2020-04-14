# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.middle_name is None:
            return super(CustomUser, self).get_full_name()
        else:
            return "%s %s. %s" % (self.first_name, self.middle_name[0], self.last_name)