# api/admin.py
from django.contrib import admin
from .models import Subject, Textbook, Topic, Quiz, Question, UserQuizScore, UserProfile

# Permite adicionar/editar questões diretamente na página do Quiz
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3 # Mostra campos para 3 novas questões por padrão

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    # Campos que aparecerão na lista de quizzes
    list_display = ('title', 'topic', 'level', 'passing_score')
    # Permite filtrar os quizzes por tópico
    list_filter = ('topic',)
    # Adiciona a seção de questões dentro da página de edição do quiz
    inlines = [QuestionInline]

# Registrando os outros modelos de forma simples
admin.site.register(Subject)
admin.site.register(Textbook)
admin.site.register(Topic)
admin.site.register(Question) # Ainda registramos para ter acesso direto se necessário
admin.site.register(UserProfile)
admin.site.register(UserQuizScore)