from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
import uuid

# ----------------- Evaluation data
class Evaluation(models.Model):
    uuid_field = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    agent = models.ForeignKey("users.Agent", on_delete=models.CASCADE, related_name="evaluated_agent")
    case_type = models.ForeignKey("evaluation.CaseType", on_delete=models.CASCADE)
    case = models.CharField(max_length=150,)
    account_name = models.CharField(max_length=150, validators=[MinLengthValidator(3)])
    contact_category = models.TextField(null=True, blank=True)
    score = models.FloatField(default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    ftr = models.BooleanField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    score_reason = models.TextField(null=True, blank=True)
    evaluator = models.ForeignKey("users.Agent", on_delete=models.CASCADE, related_name = "evaluator")
    evaluation_date = models.DateTimeField(auto_now_add=True)
    contact_date = models.DateTimeField(null=True, blank=True)
    modifier = models.ForeignKey("users.Agent", on_delete=models.CASCADE, related_name = "modified_by", null=True, blank=True)
    modification_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.case_type.case_type} -- evaluated agent: {self.agent}'

# ------------------ Evaluation Handling data
class EvaluationTimeline(models.Model):
    class Meta:
        verbose_name_plural = "Evaluation Timeline"
    evaluation = models.ForeignKey("evaluation.Evaluation", on_delete=models.CASCADE)
    modifier = models.ForeignKey("users.Agent", on_delete=models.CASCADE)
    handling_time_seconds = models.IntegerField(default=0)

# ----------------- ReAudit handling data
class ReAudit(models.Model):
    class Meta:
        verbose_name_plural = "Re-Audits"
    evaluation = models.ForeignKey("evaluation.Evaluation", on_delete=models.CASCADE)
    auditor = models.ForeignKey("users.Agent", on_delete=models.CASCADE)
    audit_date = models.DateTimeField(auto_now=True)
    previous_score = models.FloatField()
    new_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    previous_ftr = models.BooleanField(null=True, blank=True)
    new_ftr = models.BooleanField(null=True, blank=True)
    reason = models.ForeignKey("evaluation.ReAuditReason", on_delete=models.SET_NULL, null=True)

class ReAuditReason(models.Model):
    class Meta:
        verbose_name = "Re-Audit Reason"
        verbose_name_plural = "Re-Audit Reasons"
    reason = models.CharField(validators=[MinLengthValidator(5)],)



# ---------------- Mistakes data for evaluations
class EvaluationMistakes(models.Model):
    evaluation = models.ForeignKey("evaluation.Evaluation", on_delete=models.CASCADE)
    criteria = models.ForeignKey("evaluation.Criteria", on_delete=models.CASCADE)

# ---------------- Evaluation criteria
class Criteria(models.Model):
    class Meta:
        verbose_name_plural = "Criteria"
    case_type = models.ForeignKey("evaluation.CaseType", on_delete=models.CASCADE)
    criteria = models.TextField()
    comment = models.TextField(null=True, blank=True)
    scoredown = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(1.0)])
    ftr_scoredown = models.BooleanField(null=True, blank=True, default=False)
    criteria_category = models.ForeignKey("evaluation.CriteriaCategory", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.criteria

# ----------------- High level categorization for reporting
class CriteriaCategory(models.Model):
    class Meta:
        verbose_name_plural = "Criteria Categories"
    category = models.CharField()

    def __str__(self):
        return self.category

# ----------------- Case types for evaluations
class CaseType(models.Model):
    case_type = models.CharField(max_length=30, validators=[MinLengthValidator(3)])
    ftr_yn = models.BooleanField(default=False)
    team = models.ForeignKey("users.Team", on_delete=models.CASCADE)

    def __str__(self):
        return self.case_type


