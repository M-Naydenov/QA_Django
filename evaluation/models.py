from django.core.validators import MinLengthValidator
from django.db import models

# ----------------- Evaluation data
class Evaluation(models.Model):
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)
    case_type = models.ForeignKey("CaseType", on_delete=models.CASCADE)
    case = models.CharField()
    account_name = models.CharField(max_length=150, validators=[MinLengthValidator(3)])
    contact_category = models.TextField(null=True, blank=True)
    score = models.FloatField(default=1.0)
    ftr = models.NullBooleanField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    score_reason = models.TextField(null=True, blank=True)
    evaluator = models.ForeignKey("Agent", on_delete=models.CASCADE)
    evaluation_date = models.DateTimeField(auto_now_add=True)
    contact_date = models.DateTimeField(null=True, blank=True)
    modifier = models.ForeignKey("Agent", on_delete=models.CASCADE)
    modification_date = models.DateTimeField(auto_now=True)

# ------------------ Evaluation Handling data
class EvaluationTimeline(models.Model):
    evaluation = models.ForeignKey("Evaluation", on_delete=models.CASCADE)
    modifier = models.ForeignKey("Agent", on_delete=models.CASCADE)
    handling_time_seconds = models.IntegerField(default=0)

# ----------------- ReAudit handling data
class ReAudit(models.Model):
    evaluation = models.ForeignKey("Evaluation", on_delete=models.CASCADE)
    auditor = models.ForeignKey("Agent", on_delete=models.CASCADE)
    audit_date = models.DateTimeField(auto_now=True)
    previous_score = models.FloatField()
    new_score = models.FloatField()
    previous_ftr = models.NullBooleanField()
    new_ftr = models.NullBooleanField()

# ---------------- Mistakes data for evaluations
class EvaluationMistakes(models.Model):
    evaluation = models.ForeignKey("Evaluation", on_delete=models.CASCADE)
    criteria = models.ForeignKey("Criteria", on_delete=models.CASCADE)

# ---------------- Evaluation criteria
class Criteria(models.Model):
    case_type = models.ForeignKey("CaseType", on_delete=models.CASCADE)
    criteria = models.TextField()
    comment = models.TextField(null=True, blank=True)
    scoredown = models.FloatField()
    ftr_scoredown = models.NullBooleanField()

# ----------------- High level categorization for reporting
class CriteriaCategory(models.Model):
    category = models.CharField()

# ----------------- Case types for evaluations
class CaseType(models.Model):
    case_type = models.CharField(max_length=30, validators=[MinLengthValidator(3)])
    ftr_yn = models.BooleanField(default=False)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)


