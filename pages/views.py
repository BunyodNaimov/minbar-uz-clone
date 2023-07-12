from django.shortcuts import render
from rest_framework.generics import ListAPIView

from pages.models import Page
from pages.serializers import PageSerializer


class PageListAPIVew(ListAPIView):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
