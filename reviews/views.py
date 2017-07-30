# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import get_object_or_404, render
from .models import Review, Album


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def album_list(request):
    album_list = Album.objects.order_by('-name')
    context = {'album_list':album_list}
    return render(request, 'reviews/album_list.html', context)


def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'reviews/album_detail.html', {'album': album})
