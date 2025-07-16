from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from users.managers import AgentManager


# Create your models here.
# class Agent(AbstractBaseUser):
#     ...
#
#
#     objects = AgentManager()
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]
#
#     def __str__(self):
#         return 'hmm'