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
    print(user_account, user_password, user_identity)
    search_from_User = User.objects.filter(account=user_account, identity=user_identity)
    print(len(search_from_User))
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
            if user_identity == "学生":
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
                        course = CourseArrangement.objects.get(Q(course_id=i.course_id) & Q(term=time))
                        select_list.append(
                            {'name': course.course_id.course_name, 'week': course.weekday, 'time': course.session,
                             'location': course.location, 'teacher': course.teacher_id.teacher_name, 'weekday': course.week})
                except:
                    raise Http404
                return render(request, 'student/student_index.html', {'student': LoginUser, 'course_list': course_list, 'notice': notice, 'select_list': select_list})
            elif user_identity == "教师":
                #查教师表
                AccountID = user_account
                AccountType = True
                UserAccount = search_from_User[0]
                try:
                    LoginUser = Teacher.objects.get(teacher_id=user_account)
                    notice = Notice.objects.all()
                    course_arrangement = CourseArrangement.objects.filter(teacher_id__teacher_id=user_account)
                except:
                    raise Http404
                return render(request, 'teacher/teacher_index.html', {'teacher': LoginUser, 'notice': notice, 'course_arrangement': course_arrangement})
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
            if user_identity == '学生':
                context['checkedStudent'] = True
            elif user_identity == '教师':
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
        if user_identity == '学生':
            context['checkedStudent'] = True
        elif user_identity == '教师':
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

    if user_identity == '学生':
        context['checkedStudent'] = True
    elif user_identity == '教师':
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
    if user_identity == "学生":
        user = User.objects.create(account=user_account, password=user_password, identity=user_identity, phone=user_phone, email=user_email)
        student = Student.objects.create(student_id=user_account)

    elif user_identity == "教师":
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
    if status == '0':
        student = Student.objects.get(student_id=id)
        is_fix = False
        user = User.objects.get(Q(account=id) & Q(identity='学生'))
        return render(request, 'student/student_information_fix.html', {'student': student, 'user': user, 'is_fix': is_fix})
    elif status == '1':
        student = Student.objects.get(student_id=id)
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
            course = CourseArrangement.objects.get(Q(course_id=i.course_id) & Q(term=time))
            course_list.append({'name': course.course_id.course_name, 'week': course.weekday, 'time': course.session, 'location': course.location, 'teacher': course.teacher_id.teacher_name, 'weekday': course.week})
        return render(request, 'student/student_schedule.html', {'student': student, 'course': course_list, 'term': term})
    elif status == '2':
        student = Student.objects.get(student_id=id)
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
                grade_list.append({'id': i.course_id.course_id, 'name': i.course_id.course_name, 'grade': i.student_grade, 'college': i.course_id.course_college})
        return render(request, 'student/student_grade.html', {'grade_list': grade_list, 'student': student})
    elif status == '3':
        notice = Notice.objects.get(notice_id=id)
        return render(request, 'student/notice.html', {'notice': notice})
    elif status == '4':
        student = Student.objects.get(student_id=id)
        is_select = 0
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
        course = CourseArrangement.objects.filter(term=time)
        if SelectCourse.objects.filter(Q(student_id=id) & Q(term=time)):
            is_selected = True
            selected = SelectCourse.objects.filter(Q(student_id=id) & Q(term=time))
            for i in selected:
                count = count + 1
                selected_list.append({'course_id': i.course_id.course_id, 'course_name': i.course_id.course_name, 'count': count})

        return render(request, 'student/student_select_course.html', {'course': course, 'student': student, 'is_selected': is_selected, 'selected': selected_list, 'is_select': is_select, 'term': time})
    elif status == '5':
        notice = Notice.objects.get(notice_id=id)
        return render(request, 'teacher/notice.html', {'notice': notice})
    elif status == '6':
        teacher = Teacher.objects.get(teacher_id=id)
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
        course_list = []
        course = CourseArrangement.objects.filter(Q(term=time) & Q(teacher_id__teacher_id=id))
        for i in course:
            course_list.append({'name': i.course_id.course_name, 'week': i.weekday, 'time': i.session,
                                'location': i.location, 'teacher': i.teacher_id.teacher_name,
                                'weekday': i.week})
        return render(request, 'teacher/teacher_schedule.html',
                      {'teacher': teacher, 'course': course_list, 'term': term})
    elif status == '7':
        teacher = Teacher.objects.get(teacher_id=id)
        is_fix = False
        user = User.objects.get(Q(account=id) & Q(identity='教师'))
        return render(request, 'teacher/teacher_information_fix.html',
                      {'teacher': teacher, 'user': user, 'is_fix': is_fix})
    elif status == '8':
        pass
    elif status == '9':
        error = False
        return render(request, 'teacher/admin.html', {'error':error})

def student_submit_fix(request):
    id = request.POST['id']
    user = User.objects.get(Q(account=id) & Q(identity='学生'))
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

def teacher_submit_fix(request):
    id = request.POST['id']
    user = User.objects.get(Q(account=id) & Q(identity='教师'))
    teacher = Teacher.objects.get(teacher_id=id)
    ifmt = request.POST['ifmt']
    fix = request.POST['fix']
    is_fix = True
    if ifmt == 'name':
        teacher.teacher_name = fix
    elif ifmt == 'phone':
        user.phone = fix
    elif ifmt == 'wechat':
        teacher.teacher_wechat = fix
    elif ifmt == 'email':
        user.email = fix
    elif ifmt == 'qq':
        teacher.teacher_qq = fix
    elif ifmt == 'political_status':
        teacher.teacher_political_status = fix
    user.save()
    teacher.save()
    return render(request, 'teacher/teacher_information_fix.html', {'teacher': teacher, 'user': user, 'is_fix': is_fix})


def find_grade(request):
    id = request.POST.get('id')
    student = Student.objects.get(student_id=id)
    year = request.POST.get('year')
    number = request.POST.get('number')
    year_number = year+number

    grade = SelectCourse.objects.filter(Q(student_id=id) & Q(term=year_number))
    grade_list = []
    for i in grade:
        if int(i.student_grade) > 0:
            grade_list.append({'id': i.course_id.course_id, 'name': i.course_id.course_name, 'grade': i.student_grade, 'college': i.course_id.course_college})
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
        course = CourseArrangement.objects.get(Q(course_id=i.course_id) & Q(term=year_number))
        course_list.append({'name': course.course_id.course_name, 'week': course.weekday, 'time': course.session, 'location': course.location, 'teacher': course.teacher_id.teacher_name, 'weekday': course.week})
    return render(request, 'student/student_schedule.html', {'student': student, 'course': course_list, 'term': term})


def find_course_schedule(request):
    id = request.POST.get('id')
    teacher = Teacher.objects.get(teacher_id=id)
    year = request.POST.get('year')
    number = request.POST.get('number')
    year_number = year + number
    term = year + '学年第' + number[1] + '学期'
    select = CourseArrangement.objects.filter(Q(teacher_id__teacher_id=id) & Q(term=year_number))
    course_list = []
    for i in select:
        course_list.append({'name': i.course_id.course_name, 'week': i.weekday, 'time': i.session,
                            'location': i.location, 'teacher': i.teacher_id.teacher_name,
                            'weekday': i.week})
    return render(request, 'teacher/teacher_schedule.html', {'teacher': teacher, 'course': course_list, 'term': term})

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
        course = CourseArrangement.objects.filter(Q(course_id=course_id) & Q(term=time))
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
        course = CourseArrangement.objects.filter(Q(course_id__course_name=course_name) & Q(term=time))
        return render(request, 'student/student_select_course.html', {'student': student, 'course': course, 'selected': selected_list, 'is_selected': is_selected, })
    else:
        course = CourseArrangement.objects.filter(term=time)
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
        course = CourseArrangement.objects.filter(term=time)
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
        course = CourseArrangement.objects.filter(term=time)
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

def add_course(request):
    is_add = True
    course_id = request.POST.get('cid')
    course_name = request.POST.get('cname')
    college = request.POST.get('college')
    pre_course_id = request.POST.get('pcid')
    pre_course_name = request.POST.get('pcname')
    course_introduce = request.POST.get('introduce')
    Course.objects.create(course_id=course_id, course_name=course_name, course_college=college, course_pre_id=pre_course_id, course_pre_name=pre_course_name, course_introduction=course_introduce)
    return render(request, 'teacher/admin_add_course.html', {'is_add': is_add})

def is_admin(request):
    password = request.POST.get('password')
    if password == 'buctupupgo':
        return render(request, 'teacher/admin_index.html')
    else:
        error = True
        return render(request, 'teacher/admin.html', {'error': error})

def admin(request, status):
    college = (
        '信息科学与技术学院', '材料科学与工程学院', '机电工程学院',
        '化学工程学院', '经济管理学院', '化学学院',
        '数理学院', '文法学院', '生命科学与技术学院',
        '继续教育学院', '马克思主义学院', '国际教育学院',
        '侯德榜工程师学院', '巴黎居里工程师学院',
    )
    nation = (
        '汉族', '满族', '回族', '藏族', '维吾尔族', '苗族', '彝族',
        '壮族', '布依族', '侗族', '瑶族', '白族', '土家族',
        '哈尼族', '哈萨克族', '傣族', '傈僳族', '佤族', '畲族', '高山族',
        '拉祜族', '水族', '东乡族', '纳西族', '景颇族', '柯尔克孜族', '土族',
        '达斡尔族', '仫佬族', '羌族', '布朗族', '撒拉族', '毛南族', '仡佬族',
        '锡伯族', '阿昌族', '普米族', '朝鲜族', '塔吉克族', '怒族', '乌孜别克族',
        '俄罗斯族', '鄂温克族', '德昂族', '保安族', '裕固族', '京族', '塔塔尔族',
        '独龙族', '鄂伦春族', '赫哲族', '门巴族', '珞巴族', '基诺族', '黎族',
    )
    language = ('英语', '法语', '日语', '俄语',)
    sex = ('男', '女')
    statu = ('在读', '毕业')
    political_status = ('中共党员', '共青团员', '群众',)
    academic_title = ('助教', '讲师', '副教授', '教授',)
    degree = ('学士', '硕士', '博士',)
    if status == '1':
        is_add = False
        return render(request, 'teacher/add_student.html', {'college': college, 'nation': nation, 'language': language, 'sex': sex, 'status': statu, 'political_status': political_status, 'is_add': is_add})
    elif status == '2':
        is_add = False
        return render(request, 'teacher/add_teacher.html', {'college': college, 'nation': nation, 'sex': sex, 'political_status': political_status, 'degree': degree, 'academic_title': academic_title, 'is_add': is_add})
    elif status == '3':
        is_add = False
        return render(request, 'teacher/admin_add_course.html', {'is_add': is_add})
    elif status == '4':
        is_arrange = 0
        course = Course.objects.all().order_by('course_status')
        teacher = Teacher.objects.all()
        return render(request, 'teacher/admin_arrange_course.html', {'is_arrange': is_arrange, 'course': course, 'teacher': teacher})
    elif status == '5':
        return render(request, 'teacher/add_notice.html', {'is_add': False})

def add_notice(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    is_add = True
    Notice.objects.create(notice_title=title, notice_content=content)
    return render(request, 'teacher/add_notice.html', {'is_add': is_add})

def add_student(request):
    is_add = True
    student_id = request.POST.get('student_id')
    sex = request.POST.get('sex')
    student_college = request.POST.get('student_college')
    phone = request.POST.get('phone')
    student_come_year = request.POST.get('student_come_year')
    student_province = request.POST.get('student_province')
    student_birthday = request.POST.get('student_birthday')
    student_name = request.POST.get('student_name')
    student_nation = request.POST.get('student_nation')
    student_major = request.POST.get('student_major')
    email = request.POST.get('email')
    student_status = request.POST.get('student_status')
    student_city = request.POST.get('student_city')
    student_wechat = request.POST.get('student_wechat')
    student_age = request.POST.get('student_age')
    student_political_status = request.POST.get('student_political_status')
    student_class = request.POST.get('student_class')
    student_foreign_language = request.POST.get('student_foreign_language')
    student_high_school = request.POST.get('student_high_school')
    student_qq = request.POST.get('student_qq')
    Student.objects.create(
        student_id=student_id, student_sex=sex, student_college=student_college,
        student_city=student_city, student_name=student_name, student_class=student_class,
        student_major=student_major, student_nation=student_nation, student_qq=student_qq,
        student_status=student_status, student_wechat=student_wechat, student_come_year=student_come_year,
        student_foreign_language=student_foreign_language, student_birthday=student_birthday,
        student_high_school=student_high_school, student_province=student_province,
        student_political_status=student_political_status, student_age=student_age,
    )
    User.objects.create(
        account=student_id, password=student_id, identity='学生', phone=phone, email=email, name=student_name,
    )
    return render(request, 'teacher/add_student.html', {'is_add': is_add})

def add_teacher(request):
    is_add = True
    teacher_id = request.POST.get('teacher_id')
    sex = request.POST.get('sex')
    teacher_department = request.POST.get('teacher_department')
    phone = request.POST.get('phone')
    teacher_come_year = request.POST.get('teacher_come_year')
    teacher_province = request.POST.get('teacher_province')
    teacher_birthday = request.POST.get('teacher_birthday')
    teacher_name = request.POST.get('teacher_name')
    teacher_nation = request.POST.get('teacher_nation')
    teacher_degree = request.POST.get('teacher_degree')
    email = request.POST.get('email')
    teacher_city = request.POST.get('teacher_city')
    teacher_wechat = request.POST.get('teacher_wechat')
    teacher_age = request.POST.get('teacher_age')
    teacher_political_status = request.POST.get('teacher_political_status')
    teacher_graduate_school = request.POST.get('teacher_graduate_school')
    teacher_qq = request.POST.get('teacher_qq')
    teacher_academic_title = request.POST.get('teacher_academic_title')
    Teacher.objects.create(
        teacher_id=teacher_id, teacher_name=teacher_name, teacher_age=teacher_age,
        teacher_sex=sex, teacher_nation=teacher_nation, teacher_political_status=teacher_political_status,
        teacher_department=teacher_department, teacher_degree=teacher_degree,
        teacher_come_year=teacher_come_year, teacher_province=teacher_province,
        teacher_city=teacher_city, teacher_birthday=teacher_birthday,
        teacher_qq=teacher_qq, teacher_wechat=teacher_wechat,
        teacher_graduate_school=teacher_graduate_school,
        teacher_academic_title=teacher_academic_title,
    )
    User.objects.create(
        account=teacher_id, password=teacher_id, identity='教师', phone=phone, email=email, name=teacher_name,
    )
    return render(request, 'teacher/add_teacher.html', {'is_add': is_add})

def arrange_course(request):
    course_id = request.POST.get('course_id')
    teacher_id = request.POST.get('teacher')
    term = request.POST.get('term')
    week = request.POST.get('week')
    session = request.POST.get('session')
    location = request.POST.get('location')
    weekday = request.POST.get('weekday')
    course_status = request.POST.get('course_status')
    course = Course.objects.get(course_id=course_id)
    teacher = Teacher.objects.get(teacher_id=teacher_id)
    if len(CourseArrangement.objects.filter(Q(course_id=course) & Q(teacher_id=teacher) & Q(term=term))) == 1:
        is_arrange = 2
        cou = Course.objects.all().order_by('course_status')
        tea= Teacher.objects.all()
        return render(request, 'teacher/admin_arrange_course.html',
                  {'is_arrange': is_arrange, 'course': cou, 'teacher': tea})
    else:
        is_arrange = 1
        CourseArrangement.objects.create(course_id=course, term=term, teacher_id=teacher, week=week, weekday=weekday, session=session, location=location)
        course.course_status = course_status
        cou = Course.objects.all().order_by('course_status')
        tea = Teacher.objects.all()
        return render(request, 'teacher/admin_arrange_course.html',
                      {'is_arrange': is_arrange, 'course': cou, 'teacher': tea})


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