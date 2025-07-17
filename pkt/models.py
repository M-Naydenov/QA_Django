from django.core.validators import MinValueValidator
from django.db import models

# ---------------- Process Knowledge test identification
class ProcessKnowledgeTest(models.Model):
    QUARTER_CHOICES = [
        ("Q1", "Q1"),
        ("Q2", "Q2"),
        ("Q3", "Q3"),
        ("Q4", "Q4"),
    ]
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    year = models.IntegerField(validators=[MinValueValidator(2025)])
    quarter = models.CharField(choices=QUARTER_CHOICES, max_length=2)

# ---------------- Process Knowledge test log
class PKTs(models.Model):
    pkt = models.ForeignKey("ProcessKnowledgeTest", on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)
    score = models.FloatField()

# --------------- Process Knowledge test Questions
class Question(models.Model):
    pkt = models.ForeignKey("PKTs", on_delete=models.CASCADE)
    category = models.ForeignKey("QuestionCategory", on_delete=models.CASCADE)

# --------------- Possible Answers to questions
class PossibleAnswers(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    correct_yn = models.BooleanField()

# ---------------- Question Category (for reporting)
class QuestionCategory(models.Model):
    category = models.CharField()



