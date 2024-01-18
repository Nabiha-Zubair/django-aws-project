from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .serializer import TopicSerializer
from .models import Topic
from authentication.permissions import CanDeleteOwnObject

# Create your views here.


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, CanDeleteOwnObject]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        topic_with_followers = self.queryset.prefetch_related(
            'followers').all()
        # print('query prefetch: ', topic_with_followers[2].followers.all())
        return topic_with_followers

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        request_data = request.data.copy()
        request_data['user'] = request.user.id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        request_data = request.data.copy()
        user_field = request_data.pop('user', None)

        serializer = self.get_serializer(
            instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if user_field is not None:
            serializer.data['user'] = user_field

        return Response(serializer.data)
