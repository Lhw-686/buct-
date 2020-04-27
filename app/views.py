from django.shortcuts import render
from app.models import *
def login(request):
    return render(request, 'login.html')
def login_judge(request):

    user_account = request.POST.get('account')
    user_password = request.POST.get('password')
    user_identity = request.POST.get('identity')
    result1 = User.objects.filter(account=user_account, identity=user_identity)
    if(len(result1)==1):
        password = result1[0].password
        if user_password == password:
            if user_identity == "student":
                student = Student.objects.get(student_id=user_account)
                return render(request, 'student/student_information.html', {'student': student})
            elif user_identity == "teacher":
                teacher = Teacher.objects.get(teacher_id=user_account)
                return render(request, 'teacher/teacher_information.html', {'teacher': teacher})
        else:
            context = {
                "info": "密码错误！",
                "status": 1
            }
            return render(request, 'login.html', context=context)
    else:
        context = {
            "info": "账户不存在！",
            "status": 2
        }
        return render(request, 'login.html', context=context)
def student_information(request):
    return render(request, 'student/student_information.html')
def teacher_information(request):
    return render(request, 'teacher/teacher_information.html')
def register(request):
    return render(request, 'register.html')
def register_information(request):
    name = request.POST.get('name')
    id = request.POST.get('id')
    password = request.POST.get('password')
    identity = request.POST.get('identity')
    result1 = User.objects.filter(account=id, identity=identity)
    if len(result1) == 1:
        context = {
            "info": "该账户已注册",
            "status": "1"
        }
        return render(request, 'register.html', context=context)
    else:
        User.objects.create(account=id, password=password, identity=identity)
        context = {
            "info": "注册成功！",
            "status": "2"
        }
        if identity == 'student':
            Student.objects.create(student_id=id, student_name=name)
            return render(request, 'register.html', context=context)
        elif identity == 'teacher':
            Teacher.objects.create(teacher_id=id, teacher_name=name)
            return render(request, 'register.html', context=context)