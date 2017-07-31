# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from .models import Review, Album
from .forms import ReviewForm


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
    form = ReviewForm()
    return render(request, 'reviews/album_detail.html', {'album': album, 'form': form})

@login_required
def add_review(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user = request.user
        review = Review()
        review.album = album
        review.user = user
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:album_detail', args=(album.id,)))

    return render(request, 'reviews/album_detail.html', {'album': album, 'form': form})

@login_required
def user_review_list(request, username=None):
    if not username:
        user = request.user
    else:
        user = User.objects.filter(username=username).first()
    latest_review_list = Review.objects.filter(user=user).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'user':user}
    return render(request, 'reviews/user_review_list.html', context)

@login_required
def user_recommendation_list(request):
    return render(request, 'reviews/user_recommendation_list.html', {'username': request.user.username})

