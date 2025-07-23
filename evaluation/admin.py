from django.contrib import admin
from evaluation.models import Evaluation, ReAudit


# Register your models here.
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'case','score','ftr','contact_date','agent','evaluator']

@admin.register(ReAudit)
class ReAuditAdmin(admin.ModelAdmin):
    list_display = ['evaluation','auditor','audit_date','previous_score', 'new_score']
