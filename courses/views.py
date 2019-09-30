from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated

from courses.models import Course
from courses.serializers import CourseSerializer, CourseSignupSerializer


class IsAdminOrAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.method in SAFE_METHODS or
            request.user.is_staff
        )


class AllCoursesView(APIView):
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

    def get(self, request):
        items = Course.objects.all()
        serializer = CourseSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OneCourseView(APIView):
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

    def get(self, request, pk):
        item = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(item)
        return Response(serializer.data)

    def delete(self, request, pk):
        item = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(item)
        data = serializer.data
        item.delete()
        return Response(data)

    def put(self, request, pk):
        item = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseSignupView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSignupSerializer

    def patch(self, request, *args, **kwargs):
        request.data.clear()
        return super().patch(request, args, kwargs)

    def put(self, request, *args, **kwargs):
        return self.patch(request, args, kwargs)

