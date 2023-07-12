from django.urls import path

from pages.views import PageListAPIVew

urlpatterns = [
    path('', PageListAPIVew.as_view(), name='page_list'),
]