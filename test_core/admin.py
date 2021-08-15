from .models import AnsweredQuestion, QuestionBfi, QuestionMbti, QuestionPapi, QuestionTpa, TestAttempt, TestResult, Tester
from django.contrib import admin

# Register your models here.
admin.site.register(QuestionMbti)
admin.site.register(QuestionBfi)
admin.site.register(QuestionPapi)
admin.site.register(QuestionTpa)
admin.site.register(AnsweredQuestion)
admin.site.register(TestAttempt)
admin.site.register(TestResult)
admin.site.register(Tester)