from rest_framework import viewsets
from rest_framework.response import Response
from social.models.social import Profile
from social.serializers import ProfileSerializer
from rest_framework.pagination import PageNumberPagination


class ProfilePagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 100


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
