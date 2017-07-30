# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Album, Review

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('album', 'rating', 'user', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user']
    search_fields = ['comment']

# Register your models here.
admin.site.register(Album)
admin.site.register(Review, ReviewAdmin)
