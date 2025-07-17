from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from users.managers import AgentManager

# ------- the AGENT
class Agent(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        validators=[RegexValidator(regex=r'^[a-zA-z][a-zA-Z0-9.]+(@entaingroup.com){1}$'),]
    )
    icepor = models.CharField(
        max_length = 100,
        unique = True,
        validators=[MinLengthValidator(3), RegexValidator(regex=r'^[a-zA-Z0-9]+$'),]
    )
    first_name = models.CharField(
        max_length = 50,
        validators = [ MinLengthValidator(2), RegexValidator(regex=r'^[a-zA-Z0-9]+$')],
    )
    last_name = models.CharField(
        max_length = 50,
        validators = [ MinLengthValidator(2), RegexValidator(regex=r'^[a-zA-Z0-9]+$')],
    )
    team = models.ForeignKey("Team", on_delete=models.SET_NULL, null=True)
    tl = models.ForeignKey(
        "self",
        on_delete = models.SET_NULL,
        null = True,
        related_name = "agents"
    )
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(
        default = True,
    )
    is_staff = models.BooleanField(
        default = False,
    )

    objects = AgentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

# ---------- the agent's ROLE within the team
class Role(models.Model):
    work_title = models.CharField(max_length=50,
                                  validators= [MinLengthValidator(2), RegexValidator(regex=r'^[a-zA-Z0-9]+$')],
                                  )
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True)

# ---------- the agent's TEAM
class Team(models.Model):
    team_name = models.CharField(
        validators = [ MinLengthValidator(2), RegexValidator(regex=r'^[a-zA-Z0-9]+$')],
    )
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True)

# ---------- the team's DEPARTMENT
class Department(models.Model):
    department_name = models.CharField(
        validators = [ MinLengthValidator(2),],
    )