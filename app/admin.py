from django.contrib import admin

from app.models import *
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'student_name', 'student_age',
                    'student_sex', 'student_nation', 'student_political_status',
                    'student_come_year', 'student_college', 'student_major',
                    'student_class', 'student_province', 'student_city',
                    'student_birthday',  'student_qq',
                    'student_wechat',  'student_high_school',
                    'student_foreign_language', 'student_status'
                    ]

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'teacher_name', 'teacher_age',
                    'teacher_sex', 'teacher_nation', 'teacher_political_status',
                    'teacher_department', 'teacher_academic_title', 'teacher_degree',
                    'teacher_come_year', 'teacher_province', 'teacher_city',
                    'teacher_birthday', 'teacher_qq',
                    'teacher_wechat', 'teacher_graduate_school'
                    ]

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'course_name', 'course_status',
                    'course_college', 'course_pre_id', 'course_pre_name',
                    'course_introduction'
                    ]

class SelectCourseAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'term', 'course_id', 'student_grade']

class CourseArrangementAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'term', 'teacher_id',
                    'week_begin', 'week_end'
                    ]

class SchoolTermAdmin(admin.ModelAdmin):
    list_display = ['begin_year', 'end_year', 'number']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'student_id', 'message_content',
                    'message_send_time', 'message_status', 'message_title'
                    ]

class NoticeAdmin(admin.ModelAdmin):
    list_display = ['notice_id', 'notice_send_time', 'notice_content', 'notice_title']

class SelectListAdmin(admin.ModelAdmin):
    list_display = ['major', 'term', 'course_id', 'status']

class UserAdmin(admin.ModelAdmin):
    list_display = ['account', 'identity', 'password', 'phone', 'email']

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(SelectCourse, SelectCourseAdmin)
admin.site.register(CourseArrangement, CourseArrangementAdmin)
admin.site.register(SchoolTerm, SchoolTermAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(SelectList, SelectListAdmin)
admin.site.register(User, UserAdmin)