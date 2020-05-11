from django.contrib import admin
from django.urls import path
from app import views
from django.views.generic.base import RedirectView
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('login_judge/', views.login_judge),
    path('register_judge/', views.register_judge),
    path('register_judge_success/', views.register_judge_success),
    path('', views.login),
    path('student_index/', views.student_index),
    path('student_information_fix/', views.student_information_fix),
    path('student_submit_fix/', views.student_submit_fix),
    path('teacher_submit_fix/', views.teacher_submit_fix),
    url('login_judge/(\d+)(\d+)/$', views.student_information_fix, name='fix'),
    path('find_grade/', views.find_grade),
    path('find_schedule/', views.find_schedule),
    path('find_course_schedule/', views.find_course_schedule),
    path('find_course/', views.find_course),
    path('admin_find_course/', views.admin_find_course),
    path('add_course/', views.add_course),
    path('select_course/', views.select_course),
    path('cancel_select/', views.cancel_select),
    path('is_admin/', views.is_admin),
    url('is_admin/(\d+)/$', views.admin, name='admin'),
    path('add_notice/', views.add_notice),
    path('grade_manage/', views.grade_manage),
    path('update_grade/', views.update_grade),
    path('find_student/', views.find_student),
    path('add_student/', views.add_student),
    path('add_teacher/', views.add_teacher),
    path('arrange_course/', views.arrange_course),
    path('find_arranged_course/', views.find_arranged_course),
    path('delete_arranged_course/', views.delete_arranged_course),
    url(r'favicon.ico/', RedirectView.as_view(url=r'/static/image/favicon.ico')),
]
