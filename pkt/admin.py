from django.contrib import admin

from pkt.models import ProcessKnowledgeTest, PKTs, Question, QuestionCategory, PossibleAnswers


# Register your models here.
@admin.register(ProcessKnowledgeTest)
class ProcessKnowledgeTestAdmin(admin.ModelAdmin):
    list_display = ['pk', 'team', 'year', 'quarter']

@admin.register(PKTs)
class PKTsAdmin(admin.ModelAdmin):
    list_display = ['pkt', 'agent', 'score']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(PossibleAnswers)
class PossibleAnswersAdmin(admin.ModelAdmin):
    pass

@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    pass