from django.contrib import admin
from .models import Member, PersonalInfoExcelFile
from dorm.domains import Dorm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple    
from django.contrib.auth.models import Group

User = get_user_model()

class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []
    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.all(), 
         required=False,
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()
        self.save_m2m()
        return instance

admin.site.unregister(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ['permissions']
admin.site.register(Group, GroupAdmin)

class MemberCustomAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'name', 'status']
    list_display_links = ['id', 'username', 'name', 'status']
    readonly_fields = ('id', 'password', 'is_staff', 'is_superuser')
    search_fields = ("name", "username")
    list_filter = ['status']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        queryset = super().get_queryset(request)
        return queryset.filter(dorm__in = [request.user.dorm, Dorm.DORM_LIST[0][1]])

    # admin 페이지에서 멤버 새로 생성 시 비밀번호에 생일 자동 저장
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # 객체가 새로 생성될 때
            obj.password = obj.birthday  # password 필드에 birthday 값 저장
        super().save_model(request, obj, form, change)

class PersonalInfoExcelFiletAdmin(admin.ModelAdmin):
    list_display = ['excel_file', 'created_at']
    list_display_links = ['created_at']

admin.site.register(Member, MemberCustomAdmin)
admin.site.register(PersonalInfoExcelFile, PersonalInfoExcelFiletAdmin)
