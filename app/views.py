from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.db.models import Q
from app.models import *
from app.templates.formCheck import *
AccountID = None
AccountType = False
LoginUser = None
UserAccount = None

def hello(request):
    return HttpResponse("<h1>欢迎来到北京化工大学教务管理系统！</h1>")


def login(request):
    context = {
        "isNoAccount": False,
        "isPasswordWrite": False,
        "checkedStudent": True,
        "error": False,
    }
    return render(request, 'login.html', context=context)


def login_judge(request):
    global AccountID, AccountType, LoginUser, UserAccount
    user_account = request.POST.get('account')
    user_password = request.POST.get('password')
    user_identity = request.POST.get('identity')
    search_from_User = User.objects.filter(account=user_account, identity=user_identity)
    if(len(search_from_User)==1):
        #此账户存在于User表中
        if user_password == search_from_User[0].password:
            #密码正确
            if user_identity == "student":
                #查学生表
                AccountID = user_account
                AccountType = False
                UserAccount = search_from_User[0]
                try:
                    LoginUser = Student.objects.get(student_id=user_account)
                except:
                    raise Http404
                return render(request, 'student/student_index.html', {'student': LoginUser})
            elif user_identity == "teacher":
                #查教师表
                AccountID = user_account
                AccountType = True
                UserAccount = search_from_User[0]
                try:
                    LoginUser = Teacher.objects.get(teacher_id=user_account)
                except:
                    raise Http404
                return render(request, 'teacher/teacher_information.html', {'teacher': LoginUser})
        else:
            #密码错误
            context = {
                "isNoAccount": False,
                "isPasswordWrite": True,
                "pwdWrong": "密码错误, 请重新输入!",
                "pwd": user_password,
                "Account": user_account,
                "error": True,
            }
            if user_identity == 'student':
                context['checkedStudent'] = True
            elif user_identity == 'teacher':
                context['checkedStudent'] = False
            return render(request, 'login.html', context=context)
        pass
    else:
        #此账号不存在
        context = {
            "isNoAccount": True,
            "isPasswordWrite": False,
            "noAccount": "此账户不存在, 请检查是否输入有误！",
            "pwd": user_password,
            "Account": user_account,
            "error": True,
        }
        if user_identity == 'student':
            context['checkedStudent'] = True
        elif user_identity == 'teacher':
            context['checkedStudent'] = False
        return render(request, 'login.html', context=context)
    return HttpResponse("404")


def student_information(request):
    return render(request, 'student/student_information.html')
def teacher_information(request):
    return render(request, 'teacher/teacher_information.html')
def register(request):
    # 返回用户注册的页面
    context = {
        "isPasswordError": False,
        "isAccountError": False,
        "isEmailError": False,
        "isPhoneError": False,
        "checkedStudent": True,
    }
    return render(request, 'register.html', context=context)
def register_judge(request):
    #注册检查
    user_account = request.POST['account']
    user_password = request.POST['password']
    user_phone = request.POST['phone']
    user_email = request.POST['email']
    user_identity = request.POST['identity']

    context = {
        'Account': user_account,
        'pwd': user_password,
        'email': user_email,
        'phone': user_phone,
        'isPasswordError': False,
        'isAccountError': False,
        'isEmailError': False,
        'isPhoneError': False,
        'PasswordError': check_pwd(user_password),
        'AccountError': check_id(user_account),
        'EmailError': check_email(user_email),
        'PhoneError': check_phone(user_phone),
        'checkedStudent': True,
    }

    if user_identity == 'student':
        context['checkedStudent'] = True
    elif user_identity == 'teacher':
        context['checkedStudent'] = False
    #检查合法性
    islegal = True
    if context['PasswordError'] != "":
        islegal = False
        context['isPasswordError'] = True
    if context['AccountError'] != "":
        islegal = False
        context['isAccountError'] = True
    if context['PhoneError'] != "":
        islegal = False
        context['isPhoneError'] = True
    if context['EmailError'] != "":
        islegal = False
        context['isEmailError'] = True
    if not islegal:
        return render(request, "register.html", context=context)

    search_from_User = User.objects.filter(account=user_account, identity=user_identity)

    if len(search_from_User) > 0:
        for item in search_from_User:
            if user_account == item.account:
                context['isAccountError'] = True
                context['AccountError'] = "该账号已存在了"
        return render(request, "register.html", context=context)
    search_from_User2 = User.objects.filter(Q(phone=user_phone)|Q(email=user_email))
    if len(search_from_User2) > 0:
        print(len(search_from_User2))
        for item in search_from_User2:
            if user_phone == item.phone:
                context['isPhoneError'] = True
                context['PhoneError'] = '该手机号已被注册'
            if user_email == item.email:
                context['isEmailError'] = True
                context['EmailError'] = '该邮箱已被注册'
        return render(request, "register.html", context=context) ############

    user = None
    student = None
    teacher = None
    if user_identity == "student":
        user = User.objects.create(account=user_account, password=user_password, identity=user_identity, phone=user_phone, email=user_email)
        student = Student.objects.create(student_id=user_account)

    elif user_identity == "teacher":
        user = User.objects.create(account=user_account, password=user_password, identity=user_identity, phone=user_phone, email=user_email)
        teacher = Teacher.objects.create(teacher_id=user_account)
    user.save()
    if student:
        student.save()
    elif teacher:
        teacher.save()
    return render(request, "registerSuccess.html")


def register_judge_success(request):
    return render(request, "registerSuccess.html")

def student_index(request):
    return render(request, 'student/student_index.html')
def student_information_fix(request):
    return render(request, 'student/student_information_fix.html')







'''
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
'''