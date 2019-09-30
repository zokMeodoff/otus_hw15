from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIRequestFactory
from courses.models import Course
from courses.serializers import CourseSerializer
from django.utils.timezone import now
import json

client = Client()
request_factory = APIRequestFactory()


class TestCourse:

    @staticmethod
    def create_test_course(title='TestCourse'):
        course = Course.objects.create(
            title=title,
            price=100,
            date_start=now(),
            duration=5
        )
        return course


class CourseViewTestCase(TestCase):

    def setUp(self):
        TestCourse.create_test_course(title='TestCourse1')
        TestCourse.create_test_course(title='TestCourse2')
        self.user = User.objects.create_superuser('TestUser1111', 'admin@admin.ru', 'admin123')
        self.token = Token.objects.create(user=self.user)

    def test_OneCourseView(self):
        response_from_url = client.get('/courses/1/', HTTP_AUTHORIZATION='Token {}'.format(self.token)).content
        request = request_factory.get('/courses/1/')
        serializer_context = {
            'request': Request(request),
        }
        course = Course.objects.get(id=1)
        serializer = CourseSerializer(course, context=serializer_context)
        test_data = JSONRenderer().render(serializer.data)
        self.assertEqual(test_data, response_from_url)

    def test_CourseListView(self):
        response_from_url = client.get('/courses/', HTTP_AUTHORIZATION='Token {}'.format(self.token)).content
        request = request_factory.get('/courses/')
        serializer_context = {
            'request': Request(request),
        }
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, context=serializer_context, many=True)
        test_data = JSONRenderer().render(serializer.data)
        self.assertEqual(test_data, response_from_url)


class CourseSignupViewTestCase(TestCase):
    def setUp(self):
        self.course = TestCourse.create_test_course()
        self.user = User.objects.create_superuser('TestUser1111', 'admin@admin.ru', 'admin123')
        self.token = Token.objects.create(user=self.user)

    def test_course_signup_success(self):
        self.client.force_login(user=self.user)
        request_uri = '/courses/signup/{}/'.format(self.course.id)
        response_from_url = client.patch(request_uri, HTTP_AUTHORIZATION='Token {}'.format(self.token))
        response_json = json.loads(response_from_url.content.decode('utf-8'))
        self.assertEqual(response_json['title'], self.course.title)
        self.assertEqual(200, response_from_url.status_code)

    def test_course_signup_fail_no_such_course(self):
        self.client.force_login(user=self.user)
        request_uri = '/courses/signup/15/'
        response_from_url = client.post(request_uri, HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.assertTrue(404, response_from_url.status_code)

    def test_course_signup_fail_unauthorized_user(self):
        client.logout()
        request_uri = '/courses/signup/{}/'.format(self.course.id)
        response_from_url = client.post(request_uri)
        self.assertEqual(401, response_from_url.status_code)

