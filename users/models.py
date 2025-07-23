from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from users.managers import AgentManager

# ------- the AGENT
class Agent(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        validators=[RegexValidator(regex=r'^[a-zA-z][a-zA-Z0-9.]+(@entaingroup.com){1}$', message="Email can only contain letters, numbers and '.', followed by the company domain. "),]
    )
    icepor = models.CharField(
        max_length = 100,
        blank = True,
        null = True,
        validators=[MinLengthValidator(3), RegexValidator(regex=r'^[a-zA-Z0-9]+$', message='Icepor can only contain letters and numbers.'),]
    )
    first_name = models.CharField(
        max_length = 50,
        blank=True,
        null=True,
        validators = [ MinLengthValidator(2), RegexValidator(regex=r'^[a-zA-Z]+$', message='First name can only contain letters.'),],
    )
    last_name = models.CharField(
        max_length = 50,
        blank=True,
        null=True,
        validators = [ MinLengthValidator(2), RegexValidator(regex=r'^[a-zA-Z]+$', message='Last name can only contain letters.'),],
    )
    department = models.ForeignKey("users.Department", on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey("users.Team", on_delete=models.SET_NULL, null=True)
    tl = models.ForeignKey(
        "self",
        on_delete = models.SET_NULL,
        null = True,
        related_name = "agents"
    )
    role = models.ForeignKey(
        "users.Role",
        on_delete=models.SET_NULL,
        null=True
    )
    is_active = models.BooleanField(
        default = True,
    )
    is_staff = models.BooleanField(
        default = False,
    )

    objects = AgentManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# --------- AGENT PROXIES
class Analyst(Agent):
    class Meta:
        proxy = True
        verbose_name = 'Analyst'
        verbose_name_plural = 'Analysts'

    def save(self, *args, **kwargs):
        self.role = Role.objects.get(work_title='Analyst')
        return super().save(*args, **kwargs)


class SeniorAnalyst(Agent):
    class Meta:
        proxy = True
        verbose_name = 'Senior Analyst'
        verbose_name_plural = 'Senior Analysts'

    def save(self, *args, **kwargs):
        self.role = Role.objects.get(work_title='Senior Analyst')
        return super().save(*args, **kwargs)

class TeamLeader(Agent):
    class Meta:
        proxy = True
        verbose_name = 'Team Leader'
        verbose_name_plural = 'Team Leaders'

    def save(self, *args, **kwargs):
        self.role = Role.objects.get(work_title='Team Leader')
        return super().save(*args, **kwargs)

class DeputyManager(Agent):
    class Meta:
        proxy = True
        verbose_name = 'Deputy'
        verbose_name_plural = 'Deputies'

    def save(self, *args, **kwargs):
        self.role = Role.objects.get(work_title='Deputy')
        return super().save(*args, **kwargs)

class OperationsManager(Agent):
    class Meta:
        proxy = True
        verbose_name = 'Operations Manager'
        verbose_name_plural = 'Operations Managers'

    def save(self, *args, **kwargs):
        self.role = Role.objects.get(work_title='Operations Manager')
        return super().save(*args, **kwargs)

# ---------- the agent's ROLE within the team
class Role(models.Model):
    work_title = models.CharField(max_length=50,
                                  validators= [MinLengthValidator(2), RegexValidator(regex=r'^[a-zA-Z0-9]+$', message='Work title can only contain letters and numbers.'),],
                                  )
    department = models.ForeignKey("users.Department", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.work_title

# ---------- the agent's TEAM
class Team(models.Model):
    team_name = models.CharField(
        validators = [ MinLengthValidator(2), RegexValidator(regex=r'^[a-zA-Z0-9]+$', message="Team name can only contain letters and numbers."),],
    )
    department = models.ForeignKey("users.Department", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.team_name

# ---------- the team's DEPARTMENT
class Department(models.Model):
    department_name = models.CharField(
        validators = [ MinLengthValidator(2),],
    )

    def __str__(self):
        return self.department_name