from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.class_list, name='class_list'),
    path('classes/<int:class_id>/register/', views.register_class, name='register_class'),
    path('parents-students/', views.parent_student_view, name='parent_student'),
    path('cancel/<int:reg_id>/', views.cancel_registration, name='cancel_reg'),
]