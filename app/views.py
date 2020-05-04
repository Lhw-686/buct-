from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.db.models import Q
from app.models import *
from app.templates.formCheck import *
from datetime import *
import time
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
            year = datetime.now()
            last_year = year.year - 1
            time = str(last_year) + '-' + str(year.year)
            if year.month < 7:
                time = time + '-1'
            elif year.month < 9:
                time = time + '-2'
            else:
                time = time + '-3'
            if user_identity == "student":
                #查学生表
                AccountID = user_account
                AccountType = False
                UserAccount = search_from_User[0]
                course_list = []
                try:
                    LoginUser = Student.objects.get(student_id=user_account)
                    Course_information = SelectCourse.objects.filter(Q(student_id=user_account) & Q(term=time))
                    notice = Notice.objects.all()
                    for i in Course_information:
                        if int(i.student_grade) > 0:
                            course_list.append({'term': i.term, 'name': i.course_id.course_name, 'grade': i.student_grade})
                    select = SelectCourse.objects.filter(Q(student_id=user_account) & Q(term=time))
                    select_list = []
                    for i in select:
                        course = CourseArrangement.objects.get(course_id=i.course_id)
                        select_list.append(
                            {'name': course.course_id.course_name, 'week': course.week_begin, 'time': course.week_end,
                             'location': course.term, 'teacher': course.teacher_id.teacher_name})
                except:
                    raise Http404
                return render(request, 'student/student_index.html', {'student': LoginUser, 'course_list': course_list, 'notice': notice, 'select_list': select_list})
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
def student_information_fix(request, id, status):
    if status != '3':
        student = Student.objects.get(student_id=id)
    if status == '0':
        is_fix = False
        user = User.objects.get(account=id)
        return render(request, 'student/student_information_fix.html', {'student': student, 'user': user, 'is_fix': is_fix})
    elif status == '1':
        year = datetime.now()
        last_year = year.year - 1
        time = str(last_year) + '-' + str(year.year)
        term = time + '学年第'
        if year.month < 7:
            time = time + '-1'
            term = term + '1学期'
        elif year.month < 9:
            time = time + '-2'
            term = term + '2学期'
        else:
            time = time + '-3'
            term = term + '3学期'
        select = SelectCourse.objects.filter(Q(student_id=id) & Q(term=time))
        course_list = []
        for i in select:
            course = CourseArrangement.objects.get(course_id=i.course_id)
            course_list.append({'name': course.course_id.course_name, 'week': course.week_begin, 'time': course.week_end, 'location': course.term, 'teacher': course.teacher_id.teacher_name})
        return render(request, 'student/student_schedule.html', {'student': student, 'course': course_list, 'term': term})
    elif status == '2':
        grade_list = []
        year = datetime.now()
        last_year = year.year - 1
        time = str(last_year) + '-' + str(year.year)
        if year.month < 7:
            time = time + '-1'
        elif year.month < 9:
            time = time + '-2'
        else:
            time = time + '-3'
        select = SelectCourse.objects.filter(Q(student_id=id) & Q(term=time))
        for i in select:
            if int(i.student_grade) > 0:
                grade_list.append({'id': i.course_id.course_id, 'name': i.course_id.course_name, 'grade': i.student_grade, 'college': i.course_id.get_course_college_display})
        return render(request, 'student/student_grade.html', {'grade_list': grade_list, 'student': student})
    elif status == '3':
        notice = Notice.objects.get(notice_id=id)
        return render(request, 'student/notice.html', {'notice': notice})
    elif status == '4':
        is_select = 0
        course = Course.objects.all()
        is_selected = False
        year = datetime.now()
        last_year = year.year - 1
        time = str(last_year) + '-' + str(year.year)
        count = int(1)
        selected_list = []
        if year.month < 7:
            time = time + '-1'
        elif year.month < 9:
            time = time + '-2'
        else:
            time = time + '-3'
        if SelectCourse.objects.filter(Q(student_id=id) & Q(term=time)):
            is_selected = True
            selected = SelectCourse.objects.filter(Q(student_id=id) & Q(term=time))
            for i in selected:
                count = count + 1
                selected_list.append({'course_id': i.course_id.course_id, 'course_name': i.course_id.course_name, 'count': count})

        return render(request, 'student/student_select_course.html', {'course': course, 'student': student, 'is_selected': is_selected, 'selected': selected_list, 'is_select': is_select, 'term': time})

def student_submit_fix(request):
    id = request.POST['id']
    user = User.objects.get(account=id)
    student = Student.objects.get(student_id=id)
    ifmt = request.POST['ifmt']
    fix = request.POST['fix']
    is_fix = True
    if ifmt == 'name':
        student.student_name = fix
    elif ifmt == 'phone':
        user.phone = fix
    elif ifmt == 'wechat':
        student.student_wechat = fix
    elif ifmt == 'email':
        user.email = fix
    elif ifmt == 'qq':
        student.student_qq = fix
    elif ifmt == 'political_status':
        student.student_political_status = fix
    user.save()
    student.save()
    return render(request, 'student/student_information_fix.html', {'student': student, 'user': user, 'is_fix': is_fix})

def find_grade(request):
    id = request.POST.get('id')
    student = Student.objects.get(student_id=id)
    year = request.POST.get('year')
    number = request.POST.get('number')
    year_number = year+number

    grade = SelectCourse.objects.filter(Q(student_id=id) & Q(term=year_number) )
    grade_list = []
    for i in grade:
        if int(i.student_grade) > 0:
            grade_list.append({'id': i.course_id.course_id, 'name': i.course_id.course_name, 'grade': i.student_grade, 'college': i.course_id.get_course_college_display})
    return render(request, 'student/student_grade.html', {'grade_list': grade_list, 'student': student, })

def find_schedule(request):
    id = request.POST.get('id')
    student = Student.objects.get(student_id=id)
    year = request.POST.get('year')
    number = request.POST.get('number')
    year_number = year + number
    term = year + '学年第' + number[1] + '学期'
    select = SelectCourse.objects.filter(Q(student_id=id) & Q(term=year_number))
    course_list = []
    for i in select:
        course = CourseArrangement.objects.get(course_id=i.course_id)
        course_list.append({'name': course.course_id.course_name, 'week': course.week_begin, 'time': course.week_end, 'location': course.term, 'teacher': course.teacher_id.teacher_name})
    return render(request, 'student/student_schedule.html', {'student': student, 'course': course_list, 'term': term})
    '''后续有时间需要在课程安排表里面加入学期'''

def find_course(request):
    course_id = request.POST.get('course_id')
    course_name = request.POST.get('course_name')
    student_id = request.POST.get('id')
    student = Student.objects.get(student_id=student_id)
    is_select = 0
    year = datetime.now()
    last_year = year.year-1
    time = str(last_year) + '-' + str(year.year)
    if year.month <7:
        time = time + '-1'
    elif year.month<9:
        time = time + '-2'
    else:
        time = time + '-3'
    selected_list = []
    count = int(1)
    if course_id != '':
        course = Course.objects.filter(course_id=course_id)
        is_selected = False
        if SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time)):
            is_selected = True
            selected = SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time))
            for i in selected:
                count = count + 1
                selected_list.append({'course_id': i.course_id.course_id, 'course_name': i.course_id.course_name, 'count': count })
        return render(request, 'student/student_select_course.html', {'student': student, 'course': course, 'selected': selected_list, 'is_selected': is_selected, 'is_select': is_select, 'term': time})
    elif course_name != '':
        is_selected = False
        if SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time)):
            is_selected = True
            selected = SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time))
            for i in selected:
                count = count + 1
                selected_list.append({'course_id': i.course_id.course_id, 'course_name': i.course_id.course_name, 'count': count })
        course = Course.objects.filter(course_name=course_name)
        return render(request, 'student/student_select_course.html', {'student': student, 'course': course, 'selected': selected_list, 'is_selected': is_selected, })
    else:
        course = Course.objects.all()
        is_selected = False
        if SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time)):
            is_selected = True
            selected = SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time))
            for i in selected:
                count = count + 1
                selected_list.append(
                    {'course_id': i.course_id.course_id, 'course_name': i.course_id.course_name, 'count': count})
        return render(request, 'student/student_select_course.html',
                      {'student': student, 'course': course, 'selected': selected_list, 'is_selected': is_selected,
                       'is_select': is_select, 'term': time})


def select_course(request):
    student_id = request.POST.get('iid')
    course_id = request.POST.get('cid')
    student = Student.objects.get(student_id=student_id)
    year = datetime.now()
    last_year = year.year - 1
    time = str(last_year) + '-' + str(year.year)
    if year.month < 7:
        time = time + '-1'
    elif year.month < 9:
        time = time + '-2'
    else:
        time = time + '-3'
    count = int(1)
    selected_list = []
    if SelectCourse.objects.filter(Q(student_id=student_id) & Q(course_id=course_id) & Q(term=time)):
        is_select = 1
        course = Course.objects.all()
        is_selected = False
        if SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time)):
            is_selected = True
            selected = SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time))
            for i in selected:
                count = count + 1
                selected_list.append(
                    {'course_id': i.course_id.course_id, 'course_name': i.course_id.course_name, 'count': count})
        return render(request, 'student/student_select_course.html',
                      {'course': course, 'student': student, 'is_selected': is_selected, 'selected': selected_list,
                       'is_select': is_select, 'term': time})
    else:
        is_select = 2
        course = Course.objects.all()
        is_selected = False
        sid = Student.objects.get(student_id=student_id)
        cid = Course.objects.get(course_id=course_id)
        SelectCourse.objects.create(student_id=sid, course_id=cid, term=time, student_grade=0)
        if SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time)):
            is_selected = True
            selected = SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time))
            for i in selected:
                count = count + 1
                selected_list.append(
                    {'course_id': i.course_id.course_id, 'course_name': i.course_id.course_name, 'count': count})
        return render(request, 'student/student_select_course.html',
                      {'course': course, 'student': student, 'is_selected': is_selected, 'selected': selected_list,
                       'is_select': is_select})

def cancel_select(request):
    time = request.POST.get('term')
    student_id = request.POST.get('stuid')
    course_id = request.POST.get('couid')
    course_name = request.POST.get('couname')
    student = Student.objects.get(student_id=student_id)
    SelectCourse.objects.get(Q(student_id=student_id) & Q(course_id__course_id=course_id) & Q(term=time)).delete()
    is_select = 3
    course = Course.objects.all()
    is_selected = False
    count = int(1)
    selected_list = []
    if SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time)):
        is_selected = True
        selected = SelectCourse.objects.filter(Q(student_id=student_id) & Q(term=time))
        for i in selected:
            count = count + 1
            selected_list.append(
                {'course_id': i.course_id.course_id, 'course_name': i.course_id.course_name, 'count': count})

    return render(request, 'student/student_select_course.html',
                  {'course': course, 'student': student, 'is_selected': is_selected, 'selected': selected_list,
                   'is_select': is_select, 'term': time})


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