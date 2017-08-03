# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from .models import Review, Album, Cluster
from .forms import ReviewForm
from .suggestions import update_clusters


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
        update_clusters()
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
    # get request user reviewed albums
    user_reviews = Review.objects.filter(user=request.user).prefetch_related('album')
    user_reviews_album_ids = set(map(lambda x: x.album.id, user_reviews))

    # get request user cluster name (first one for now)
    try:
        user_cluster_name = \
            request.user.cluster_set.first().name
    except:
        update_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    # get usernames for other members of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(id=request.user.id).all()
    other_members_user_ids = set(map(lambda x: x.id, user_cluster_other_members))

    # get reviews by those users, excluding albums reviewed by current user
    # get album ids
    other_users_reviews = \
        Review.objects.filter(user_id__in=other_members_user_ids) \
            .exclude(album__id__in=user_reviews_album_ids)
    other_users_reviews_album_ids = set(map(lambda x: x.album.id, other_users_reviews))
    # get an album list, ordered by rating, including previous ids
    album_list = sorted(
        list(Album.objects.filter(id__in=other_users_reviews_album_ids)),
        key=lambda x: x.average_rating,
        reverse=True
    )
    return render(
        request,
        'reviews/user_recommendation_list.html',
        {'username': request.user.username, 'album_list': album_list}
    )

