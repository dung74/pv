Bước 1: Khởi động các dịch vụ (Backend, Database)Mở terminal tại thư mục gốc và chạy:Bashdocker-compose up --build -d
Bước 2: Thiết lập Database và Dữ liệu mẫu Chạy các lệnh sau để khởi tạo bảng và nạp dữ liệu (2 Parents, 3 Students, 2-3 Classes): 
    # Thực hiện migrate database
    docker-compose exec backend python manage.py migrate
    
    # Nạp dữ liệu mẫu (Seed data)
    docker-compose exec backend python manage.py loaddata seed.json
    
    # (Tùy chọn) Tạo tài khoản admin để quản lý
    docker-compose exec backend python manage.py createsuperuser
    
    # Nạp dữ liệu mẫu (Seed data)
    docker-compose exec backend python manage.py loaddata seed.json

    # (Tùy chọn) Tạo tài khoản admin để quản lý
    docker-compose exec backend python manage.py createsuperuser
3. Các Endpoint chính & Truy cập
    Giao diện người dùng: http://localhost:8000/classes/
   Trang quản trị (Admin): http://localhost:8000/admin/
   RESTful API:   GET /api/parents/: Danh sách phụ huynh.
                 GET /api/students/: Danh sách học sinh. GET /api/classes/:
                 Danh sách lớp học. POST /api/classes/<id>/register/: Đăng ký học sinh vào lớp (Có check sĩ số, trùng lịch và gói học).


4. Cấu trúc Project /api: Chứa logic nghiệp vụ Django (Models, Views, Serializers). /core: Cấu hình hệ thống Django.Dockerfile & docker-compose.yml: Cấu hình containerization. seed.json: Dữ liệu mẫu phục vụ test nhanh. 
