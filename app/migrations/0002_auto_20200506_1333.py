# Generated by Django 2.2.11 on 2020-05-06 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_college',
            field=models.CharField(default='信息科学与技术学院', max_length=20, verbose_name='开课学院'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_status',
            field=models.CharField(default='未开', max_length=20, verbose_name='课程状态'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='notice_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_college',
            field=models.CharField(default='信息科学与技术学院', max_length=20, null=True, verbose_name='学院'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_foreign_language',
            field=models.CharField(default='英语', max_length=20, null=True, verbose_name='外语'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_nation',
            field=models.CharField(default='汉族', max_length=20, null=True, verbose_name='民族'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_political_status',
            field=models.CharField(default='群众', max_length=20, null=True, verbose_name='政治面貌'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_sex',
            field=models.CharField(default='男', max_length=20, null=True, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_status',
            field=models.CharField(default='在读', max_length=20, null=True, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_academic_title',
            field=models.CharField(default='教授', max_length=20, null=True, verbose_name='职称'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_degree',
            field=models.CharField(default='学士', max_length=20, null=True, verbose_name='学位'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_department',
            field=models.CharField(default='信息科学与技术学院', max_length=20, null=True, verbose_name='学院'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_nation',
            field=models.CharField(default='汉族', max_length=20, null=True, verbose_name='民族'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_political_status',
            field=models.CharField(default='群众', max_length=20, null=True, verbose_name='政治面貌'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_sex',
            field=models.CharField(default='男', max_length=20, null=True, verbose_name='性别'),
        ),
    ]
