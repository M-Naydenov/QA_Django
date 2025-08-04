
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users.forms import CreateUserForm, UpdateUserForm
from users.models import Team, TeamLeader, Department, Analyst, SeniorAnalyst, DeputyManager, OperationsManager, Role

# Register your models here.
UserModel = get_user_model()


@admin.register(UserModel)
class AgentAdmin(UserAdmin):
    model = UserModel
    add_form = CreateUserForm
    form = UpdateUserForm
    list_display = ('email', 'icepor', 'first_name', 'last_name', 'role','team', 'tl')
    ordering = ('email',)
    fieldsets = (
            (
                'Login Details', {
                'classes': ('wide',),
                'fields': ('email', 'password'),
            }
            ),

             (
                 'Personal Details', {
                 'classes': ('wide',),
                 'fields': ('icepor', 'first_name', 'last_name'),
             }
             ),

             (
                 'Team Affiliation', {
                 'classes': ('wide',),
                 'fields': ('department', 'team', 'tl', 'role'),
             }
             ),
    )
    add_fieldsets = (
            (
                'Login Details', {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            }),
            (
                'Team Affiliation', {
                'fields': ( 'department', 'team', 'tl', 'role')
                }
            ),
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['pk','team_name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['pk','department_name']

@admin.register(Analyst)
class AnalystAdmin(AgentAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(role__work_title='Analyst')

@admin.register(SeniorAnalyst)
class SeniorAnalystAdmin(AgentAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(role__work_title='Senior Analyst')

@admin.register(TeamLeader)
class TeamLeaderAdmin(AgentAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(role__work_title='Team Leader')

@admin.register(DeputyManager)
class DeputyManagerAdmin(AgentAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(role__work_title='Deputy Manager')

@admin.register(OperationsManager)
class OperationsManagerAdmin(AgentAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(role__work_title='Operations Manager')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['pk','work_title', 'department']