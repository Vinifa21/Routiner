# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importando todas as views que criamos
from .views import (
    SubjectViewSet,
    TextbookViewSet,
    TopicViewSet,
    QuizQuestionsView,
    SubmitQuizView,
    UserDashboardView,
    UserHistoryView,
    UserProfileView
)

# O Router cria automaticamente as URLs para os ViewSets.
# Ex: /subjects/, /subjects/{id}/, /topics/, /topics/{id}/ etc.
router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'textbooks', TextbookViewSet, basename='textbook')
router.register(r'topics', TopicViewSet, basename='topic')

# urlpatterns define as rotas da nossa API.
urlpatterns = [
    # Inclui as URLs geradas automaticamente pelo router
    path('', include(router.urls)),

    # ======================================================= #
    # URLs para a lógica de Quiz e Exercícios
    # ======================================================= #

    # Rota para buscar as questões de um quiz específico.
    # Exemplo de requisição: GET /api/quizzes/1/questions/
    path('quizzes/<int:quiz_id>/questions/', QuizQuestionsView.as_view(), name='quiz-questions'),

    # Rota para submeter as respostas de um quiz.
    # Exemplo de requisição: POST /api/quizzes/1/submit/
    path('quizzes/<int:quiz_id>/submit/', SubmitQuizView.as_view(), name='quiz-submit'),

    # ======================================================= #
    # URLs para o Painel do Usuário
    # ======================================================= #

    # Rota para buscar os dados do dashboard (streak, metas, etc).
    # Exemplo de requisição: GET /api/dashboard/
    path('dashboard/', UserDashboardView.as_view(), name='user-dashboard'),

    # Rota para buscar o histórico de atividades do usuário.
    # Exemplo de requisição: GET /api/history/
    path('history/', UserHistoryView.as_view(), name='user-history'),

    # Rota para visualizar e atualizar o perfil do usuário (meta diária).
    # Exemplo de requisição: GET ou PUT/PATCH /api/profile/
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]