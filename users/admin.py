from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.
UserModel = get_user_model()


@admin.register(UserModel)
class AgentAdmin(admin.ModelAdmin):
    pass
