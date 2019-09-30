from rest_framework import serializers
from courses.models import Course, Teacher, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'date', 'homework', 'course')


class CourseSerializer(serializers.ModelSerializer):
    lessons = serializers.StringRelatedField(many=True)
    teachers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'price', 'date_start', 'duration', 'teachers', 'lessons')


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'about')


class CourseSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'students')
        extra_kwargs = {'students': {'write_only': True}}

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user not in instance.students.all():
            instance.students.add(user)
        return instance
