from django.contrib import admin

# Register your models here.
from django.db.models import QuerySet, Count, F

from polling_app.models import Poll, Question, Choice


class QuestionInline(admin.StackedInline):
    model = Question


class PollAdmin(admin.ModelAdmin):
    list_display = ['name', 'questions_count', 'get_desc']
    inlines = [
        # QuestionInline
    ]

    def get_queryset(self, request):
        qs: QuerySet = super().get_queryset(request)
        qs = qs.annotate(length=Count('question'))
        return qs

    def questions_count(self, obj):
        return obj.length

    def get_desc(self, obj):
        return obj.desc


admin.site.register(Poll, PollAdmin)


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    preserve_filters = True
    list_display = ['text', 'kind', 'choices_len', 'poll_name']
    list_filter = (
        'poll__name',
        # 'kind',
    )
    search_fields = ('text', )
    inlines = [
        ChoiceInline
    ]

    def get_queryset(self, request):
        qs: QuerySet = super().get_queryset(request)
        qs = qs.annotate(choices_len=Count('choices'))
        qs = qs.annotate(poll_name=F('poll__name'))
        return qs

    def choices_len(self, x):
        return x.choices_len

    def poll_name(self, x):
        return x.poll_name


admin.site.register(Question, QuestionAdmin)

# admin.site.register(Question)
