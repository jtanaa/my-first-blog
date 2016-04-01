from django.contrib import admin

# Register your models here.
from .models import Question, Choice

class ChoiceInliness(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Date information',{'fields':['pub_date'],'classes':['collapse']}),
        ]
    inlines = [ChoiceInliness]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter=['pub_date']
    list_per_page = 50
    search_fields = ['question_text']

# class QuestionModelAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Main information', {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']}),
#     ]
#     search_fields = ['question_text']
#     class Meta:
#         model = Question


# class ChoiceModelAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'question']
#     search_fields = ['choice_text']
#     class Meta:
#         model = Choice

admin.site.register(Question, QuestionAdmin)

