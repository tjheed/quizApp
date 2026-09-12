from django.contrib import admin
from .models import Topic, Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4 # Shows 4 choice fields by default when adding a question

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Topic)
admin.site.register(Question, QuestionAdmin)