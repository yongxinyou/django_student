from django.contrib import admin
from poll.models import Subject, Teacher


class SubjectModelAdmin(admin.ModelAdmin):
    """学科的模型管理类"""
    list_display = ('no', 'name', 'intro')
    ordering = ('no', )


class TeacherModelAdmin(admin.ModelAdmin):
    """老师模型管理"""
    list_display = ('no', 'name', 'gender', 'birth', 'good_count', 'bad_count', 'subject')
    ordering = ('no', )
    list_filter = ('name', )
    search_fields = ('name', )


admin.site.register(Subject, SubjectModelAdmin)
admin.site.register(Teacher, TeacherModelAdmin)