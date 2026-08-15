
from django.urls import path
from .views import *

urlpatterns = [
    path('about/', about, name='about'),
    path('save/', save.as_view(), name='save'),
    path('', mainHome.as_view(), name='homePage'),
    path('category/<slug:tag_slug>/', category.as_view(), name='category'),
    path('card/<slug:tag_slug>/', card.as_view(), name='card'),
    path('search/', search.as_view(), name='ajax_search'),
    path('head/', header, name='head'),
    path('gallery/<slug:tag_slug>/', gallery, name='gallery'),
]