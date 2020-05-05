from django.db import models

# Create your models here.

sex = (
        ('male', '男'),
        ('female', '女'),
    )
ident = (
        ('student', '学生'),
        ('teacher', '教师'),
    )
college = (
    ('1', '信息科学与技术学院'), ('2', '材料科学与工程学院'), ('3', '机电工程学院'),
    ('4', '化学工程学院'), ('5', '经济管理学院'), ('6', '化学学院'),
    ('7', '数理学院'), ('8', '文法学院'), ('9', '生命科学与技术学院'),
    ('10', '继续教育学院'), ('11', '马克思主义学院'), ('12', '国际教育学院'),
    ('13', '侯德榜工程师学院'), ('14', '巴黎居里工程师学院'),
)
status = (
    ('1', '在读'),
    ('2', '毕业')
)
political_status = (
    ('1', '中共党员'),
    ('2', '共青团员'),
    ('3', '群众'),
)
nation = (
    ('1', '汉族'), ('2', '满族'), ('3', '回族'), ('4', '藏族'), ('5', '维吾尔族'), ('6', '苗族'), ('7', '彝族'),
    ('8', '壮族'), ('9', '布依族'), ('10', '侗族'), ('11', '瑶族'), ('12', '白族'), ('14', '土家族'),
    ('15', '哈尼族'), ('16', '哈萨克族'), ('17', '傣族'), ('18', '傈僳族'), ('19', '佤族'), ('20', '畲族'), ('21', '高山族'),
    ('22', '拉祜族'), ('23', '水族'), ('24', '东乡族'), ('25', '纳西族'), ('26', '景颇族'), ('27', '柯尔克孜族'), ('28', '土族'),
    ('29', '达斡尔族'), ('30', '仫佬族'), ('31', '羌族'), ('32', '布朗族'), ('33', '撒拉族'), ('34', '毛南族'), ('35', '仡佬族'),
    ('36', '锡伯族'), ('37', '阿昌族'), ('38', '普米族'), ('39', '朝鲜族'), ('40', '塔吉克族'), ('41', '怒族'), ('42', '乌孜别克族'),
    ('43', '俄罗斯族'), ('44', '鄂温克族'), ('45', '德昂族'), ('46', '保安族'), ('47', '裕固族'), ('48', '京族'), ('49', '塔塔尔族'),
    ('50', '独龙族'), ('51', '鄂伦春族'), ('52', '赫哲族'), ('53', '门巴族'), ('54', '珞巴族'), ('55', '基诺族'), ('56', '黎族'),
)
language = (
    ('1', '英语'),
    ('2', '法语'),
    ('3', '日语'),
    ('4', '俄语'),
)
academic_title = (
    ('1', '助教'), ('2', '讲师'),
    ('3', '副教授'), ('4', '教授'),
)
degree = (
    ('1', '学士'), ('2', '硕士'), ('3', '博士'),
)
class Student(models.Model):

    '''学生信息表'''

    student_id = models.CharField(max_length=20, verbose_name='学号', primary_key=True, unique=True, db_index=True)
    student_name = models.CharField(max_length=20, verbose_name='姓名', null=True)
    student_age = models.PositiveSmallIntegerField(verbose_name='年龄', null=True)
    student_sex = models.CharField(max_length=20, choices=sex, default='男', verbose_name='性别', null=True)
    student_nation = models.CharField(max_length=20, choices=nation, default='汉族', verbose_name='民族', null=True)
    student_political_status = models.CharField(max_length=20, choices=political_status, default='群众', verbose_name='政治面貌', null=True)
    student_come_year = models.DateField(verbose_name='入学日期', null=True)
    student_college = models.CharField(max_length=20, choices=college, default='信息科学与技术学院', verbose_name='学院', null=True)
    student_major = models.CharField(max_length=20, verbose_name='专业', null=True)
    student_class = models.CharField(max_length=20, verbose_name='班级', null=True)
    student_province = models.CharField(max_length=20, verbose_name='省份', null=True)
    student_city = models.CharField(max_length=20, verbose_name='城市', null=True)
    student_birthday = models.DateField(verbose_name='出生日期', null=True)
    #student_phone = models.CharField(max_length=20, verbose_name='手机号码', null=True)
    student_qq = models.CharField(max_length=20, verbose_name='QQ号码', null=True)
    student_wechat = models.CharField(max_length=20, verbose_name='微信号码', null=True)
    #student_email = models.EmailField(verbose_name='邮件地址', null=True)
    student_high_school = models.CharField(max_length=20, verbose_name='毕业高中', null=True)
    student_foreign_language = models.CharField(max_length=20, choices=language, default='英语', verbose_name='外语', null=True)
    student_status = models.CharField(max_length=20, choices=status, default='在读', verbose_name='状态', null=True)
    #student_image

    class Meta:
        verbose_name = '学生信息表'
        verbose_name_plural = verbose_name

class Teacher(models.Model):

    '''教师信息表'''

    teacher_id = models.CharField(max_length=20, verbose_name='工号', primary_key=True, unique=True, db_index=True)
    teacher_name = models.CharField(max_length=20, verbose_name='姓名', null=True)
    teacher_age = models.PositiveSmallIntegerField(verbose_name='年龄', null=True)
    teacher_sex = models.CharField(max_length=20, choices=sex, default='男', verbose_name='性别', null=True)
    teacher_nation = models.CharField(max_length=20, choices=nation, default='汉族', verbose_name='民族', null=True)
    teacher_political_status = models.CharField(max_length=20, choices=political_status, default='群众', verbose_name='政治面貌', null=True)
    teacher_department = models.CharField(max_length=20, verbose_name='学院', choices=college, default='信息科学与技术学院', null=True)
    teacher_academic_title = models.CharField(max_length=20, choices=academic_title, default='教授', verbose_name='职称', null=True)
    teacher_degree = models.CharField(max_length=20, choices=degree, default='学士', verbose_name='学位', null=True)
    teacher_come_year = models.DateTimeField(verbose_name='入职日期', null=True) #去掉time
    teacher_province = models.CharField(max_length=20, verbose_name='省份', null=True)
    teacher_city = models.CharField(max_length=20, verbose_name='城市', null=True)
    teacher_birthday = models.DateTimeField(verbose_name='出生日期', null=True) #去掉time
    #teacher_phone = models.CharField(max_length=20, verbose_name='手机号码', null=True)
    teacher_qq = models.CharField(max_length=20, verbose_name='QQ号码', null=True)
    teacher_wechat = models.CharField(max_length=20, verbose_name='微信号码', null=True)
    #teacher_email = models.EmailField(verbose_name='邮件地址', null=True)
    teacher_graduate_school = models.CharField(max_length=20, verbose_name='毕业院校', null=True)

    class Meta:
        verbose_name = '教师信息表'
        verbose_name_plural = verbose_name

class Course(models.Model):
    '''课程信息表'''
    course_id = models.CharField(max_length=20, verbose_name='课程号', primary_key=True, unique=True, db_index=True)
    course_name = models.CharField(max_length=20, verbose_name='课程名', unique=True)
    course_status = models.CharField(max_length=20, verbose_name='课程状态')
    course_college = models.CharField(max_length=20, choices=college, default='信息科学与技术', verbose_name='开课学院')
    course_pre_id = models.CharField(max_length=20, verbose_name='先修课程号')
    course_pre_name = models.CharField(max_length=20, verbose_name='先修课程名')
    course_introduction = models.CharField(max_length=1000, verbose_name='课程介绍')

    class Meta:
        verbose_name = '课程信息表'
        verbose_name_plural = verbose_name

class SelectCourse(models.Model):
    '''选课表'''
    student_id = models.ForeignKey(to='Student', on_delete=models.DO_NOTHING, verbose_name='学号')
    term = models.CharField(max_length=20, verbose_name='学期')
    course_id = models.ForeignKey(to='Course',  on_delete=models.DO_NOTHING, verbose_name='课程号')
    student_grade = models.CharField(max_length=20, verbose_name='成绩')

    class Meta:
        verbose_name = '选课表'
        verbose_name_plural = verbose_name
        unique_together = ('student_id', 'term', 'course_id',)

class CourseArrangement(models.Model):
    '''课程安排表'''
    course_id = models.ForeignKey(to='Course', on_delete=models.DO_NOTHING, verbose_name='课程号')
    term = models.CharField(max_length=20, verbose_name='学期')
    teacher_id = models.ForeignKey(to='Teacher', on_delete=models.DO_NOTHING, verbose_name='工号')
    week = models.CharField(max_length=20, verbose_name='周次')
    session = models.CharField(max_length=20, verbose_name='节次')
    location = models.CharField(max_length=20, verbose_name='地点')
    weekday = models.CharField(max_length=20, verbose_name='上课日期')


    class Meta:
        verbose_name = '课程安排表'
        verbose_name_plural = verbose_name
        unique_together = ('course_id', 'term', 'teacher_id',)


class SchoolTerm(models.Model):
    '''学期表（搁置）'''
    begin_year = models.CharField(max_length=20, verbose_name='开始年份')
    end_year = models.CharField(max_length=20, verbose_name='结束年份')
    number = models.IntegerField(verbose_name='学期号')

    class Meta:
        verbose_name = '学期表'
        verbose_name_plural = verbose_name
        unique_together = ('begin_year', 'end_year', 'number',)

class Message(models.Model):
    '''消息表(搁置)'''
    message_id = models.CharField(max_length=20, verbose_name='消息号', primary_key=True, unique=True, db_index=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING, verbose_name='学号')
    message_content = models.CharField(max_length=1000, verbose_name='消息内容')
    message_send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送日期')
    message_status = models.CharField(max_length=20, verbose_name='消息状态')
    message_title = models.CharField(max_length=255, verbose_name='消息标题')

    class Meta:
        verbose_name = '消息表'
        verbose_name_plural = verbose_name

class Notice(models.Model):
    '''公告表'''
    notice_id = models.CharField(max_length=20, verbose_name='通知号', primary_key=True, unique=True, db_index=True)
    notice_send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送日期')
    notice_content = models.CharField(max_length=1000, verbose_name='通知内容')
    notice_title = models.CharField(max_length=255, verbose_name='通知标题')

    class Meta:
        verbose_name = '公告表'
        verbose_name_plural = verbose_name

class SelectList(models.Model):
    '''选课清单表'''
    major =  models.CharField(max_length=20, verbose_name='专业')
    term = models.CharField(max_length=20, verbose_name='学期')
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='课程号')
    status = models.CharField(max_length=20, verbose_name='状态')
    volume = models.IntegerField(verbose_name='容量')

    class Meta:
        verbose_name = '选课清单表'
        verbose_name_plural = verbose_name
        unique_together = ('major', 'term',)

class User(models.Model):
    '''用户登录表'''
    account = models.CharField(max_length=20, verbose_name='账号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    identity = models.CharField(max_length=20, choices=ident, default='学生', verbose_name='身份')
    password = models.CharField(max_length=32, verbose_name='密码')
    phone = models.CharField(max_length=11, verbose_name='手机号码', unique=True)
    email = models.EmailField(verbose_name='邮件地址', unique=True)

    class Meta:
        verbose_name = '用户登录表'
        verbose_name_plural = verbose_name
        unique_together = ('account', 'identity',)

