from django.contrib import admin
from evaluation.models import Evaluation, ReAudit, CaseType, Criteria, EvaluationTimeline, CriteriaCategory, \
    EvaluationMistakes
from users.models import Team


# Register your models here.
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'uuid_field', 'case','score','ftr','contact_date','agent','evaluator']

@admin.register(ReAudit)
class ReAuditAdmin(admin.ModelAdmin):
    list_display = ['evaluation','auditor','audit_date','previous_score', 'new_score']

@admin.register(CaseType)
class CaseTypeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'case_type', 'team', 'ftr_yn']

@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ['case_type', 'criteria', 'criteria_category', 'scoredown', 'ftr_scoredown']

@admin.register(EvaluationTimeline)
class EvaluationTimelineAdmin(admin.ModelAdmin):
    list_display = ['evaluation', 'modifier', 'handling_time_seconds']

@admin.register(CriteriaCategory)
class CriteriaCategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category']

@admin.register(EvaluationMistakes)
class EvaluationMistakesAdmin(admin.ModelAdmin):
    list_display = ['pk','evaluation','criteria']

