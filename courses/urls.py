from django.urls import path
from courses.views import AllCoursesView, OneCourseView, CourseSignupView


app_name = 'courses'

urlpatterns = [
    path('', AllCoursesView.as_view(), name='courses'),
    path('<int:pk>/', OneCourseView.as_view(), name='course'),
    path('signup/<int:pk>/', CourseSignupView.as_view()),
]