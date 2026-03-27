from rest_framework import serializers
from .models import Parent, Student, Class, Subscription, ClassRegistration

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    parent_info = ParentSerializer(source='parent', read_only=True) # Để xem chi tiết parent [cite: 28]
    class Meta:
        model = Student
        fields = ['id', 'name', 'dob', 'gender', 'current_grade', 'parent', 'parent_info']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class ClassRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRegistration
        fields = '__all__'