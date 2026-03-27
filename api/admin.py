from django.contrib import admin
from .models import Parent, Student, Class, ClassRegistration, Subscription

admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(ClassRegistration)
admin.site.register(Subscription)