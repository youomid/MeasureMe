# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-02 15:28
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import User 

def create_guest_user(apps, schema_editor):
	"""
	Create a guest user for login.
	"""

	User.objects.create_superuser('guest', 'guest@example.com', 'guest')


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
	    migrations.RunPython(create_guest_user),
    ]
