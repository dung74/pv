from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from psycopg2 import IntegrityError
from .models import Parent, Student, Class, ClassRegistration, Subscription


# 1. Giao diện danh sách lớp & Đăng ký
def class_list(request):
    context = {
        'classes': Class.objects.all(),
        'students': Student.objects.all(),
        'days': [
            (0, 'Thứ 2'), (1, 'Thứ 3'), (2, 'Thứ 4'),
            (3, 'Thứ 5'), (4, 'Thứ 6'), (5, 'Thứ 7'), (6, 'Chủ nhật')
        ]
    }
    return render(request, 'api/class_list.html', context)


def parent_student_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # ---------------------------
        # TẠO PHỤ HUYNH
        # ---------------------------
        if action == 'create_parent':
            email = request.POST.get('email')

            # Kiểm tra email trùng trước khi lưu
            if Parent.objects.filter(email=email).exists():
                messages.error(request, "Email đã tồn tại, vui lòng dùng email khác!")
                return redirect('parent_student')

            # Email không trùng → tạo parent
            Parent.objects.create(
                name=request.POST.get('name'),
                phone=request.POST.get('phone'),
                email=email
            )
            messages.success(request, "Tạo phụ huynh thành công!")
            return redirect('parent_student')

        # ---------------------------
        # TẠO HỌC SINH
        # ---------------------------
        elif action == 'create_student':
            name = request.POST.get('name')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            current_grade = request.POST.get('current_grade')
            parent_id = request.POST.get('parent_id')

            # -------- Check missing fields ----------
            if not name or not dob or not gender or not current_grade or not parent_id:
                messages.error(request, "Vui lòng nhập đầy đủ thông tin học sinh!")
                return redirect('parent_student')

            parent = get_object_or_404(Parent, id=parent_id)

            Student.objects.create(
                name=name,
                dob=dob,
                gender=gender,
                current_grade=current_grade,
                parent=parent
            )
            messages.success(request, "Tạo học sinh thành công!")
            return redirect('parent_student')

    context = {
        'parents': Parent.objects.all(),
        'students': Student.objects.all(),
        'registrations': ClassRegistration.objects.all()
    }
    return render(request, 'api/parent_student.html', context)



# 2. Đăng ký lớp
def register_class(request, class_id):
    if request.method == 'POST':
        target_class = get_object_or_404(Class, id=class_id)
        student = get_object_or_404(Student, id=request.POST.get('student_id'))

        # Kiểm tra sĩ số
        if target_class.registrations.count() >= target_class.max_students:
            messages.error(request, f"Lớp {target_class.name} đã đầy!")
            return redirect('class_list')

        # Kiểm tra trùng lịch
        overlap = ClassRegistration.objects.filter(
            student=student,
            classroom__day_of_week=target_class.day_of_week,
            classroom__time_slot=target_class.time_slot
        ).exists()
        if overlap:
            messages.error(request, "Học sinh đã có lớp khác vào khung giờ này!")
            return redirect('class_list')

        # Kiểm tra gói học
        sub = Subscription.objects.filter(
            student=student,
            end_date__gte=timezone.now().date()
        ).last()

        if not sub or sub.used_sessions >= sub.total_sessions:
            messages.error(request, "Gói học hết hạn hoặc hết buổi!")
            return redirect('class_list')

        # Lưu đăng ký và trừ buổi
        ClassRegistration.objects.create(classroom=target_class, student=student)
        sub.used_sessions += 1
        sub.save()

        messages.success(request, "Đăng ký thành công!")

    return redirect('class_list')



# 3. Hủy đăng ký lớp
def cancel_registration(request, reg_id):
    reg = get_object_or_404(ClassRegistration, id=reg_id)

    # Hoàn buổi (nếu có gói học)
    sub = Subscription.objects.filter(student=reg.student).last()
    if sub and sub.used_sessions > 0:
        sub.used_sessions -= 1
        sub.save()
        messages.info(request, "Đã hủy và hoàn trả 1 buổi vào gói học.")

    reg.delete()
    return redirect('parent_student')