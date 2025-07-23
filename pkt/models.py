from django.core.validators import MinValueValidator
from django.db import models

# ---------------- Process Knowledge test identification
class ProcessKnowledgeTest(models.Model):
    class Meta:
        verbose_name = 'PKT instance'
        verbose_name_plural = "PKT instances"
    QUARTER_CHOICES = [
        ("Q1", "Q1"),
        ("Q2", "Q2"),
        ("Q3", "Q3"),
        ("Q4", "Q4"),
    ]
    team = models.ForeignKey("users.Team", on_delete=models.CASCADE)
    year = models.IntegerField(validators=[MinValueValidator(2025)])
    quarter = models.CharField(choices=QUARTER_CHOICES, max_length=2)

    def __str__(self):
        return f"{self.quarter} - {self.year}"

# ---------------- Process Knowledge test log
class PKTs(models.Model):
    class Meta:
        verbose_name = 'PKT'
        verbose_name_plural = "PKT Log"
    pkt = models.ForeignKey("pkt.ProcessKnowledgeTest", on_delete=models.CASCADE)
    agent = models.ForeignKey("users.Agent", on_delete=models.CASCADE)
    score = models.FloatField()

# --------------- Process Knowledge test Questions
class Question(models.Model):
    pkt = models.ForeignKey("pkt.PKTs", on_delete=models.CASCADE)
    category = models.ForeignKey("pkt.QuestionCategory", on_delete=models.CASCADE)

# --------------- Possible Answers to questions
class PossibleAnswers(models.Model):
    class Meta:
        verbose_name = 'Possible Answer'
        verbose_name_plural = "Possible Answers"
    question = models.ForeignKey("pkt.Question", on_delete=models.CASCADE)
    correct_yn = models.BooleanField()

# ---------------- Question Category (for reporting)
class QuestionCategory(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Question Categories"
    category = models.CharField()



