from django.shortcuts import render

# api/views.py

from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

# Importando todos os modelos e serializadores necessários
from .models import (
    Subject, Textbook, Topic, Quiz, Question,
    UserQuizScore, UserProfile, UserActivity
)
from .serializers import (
    SubjectSerializer, TextbookSerializer, TopicSerializer,
    QuestionSerializer, UserProfileSerializer, UserActivitySerializer
)


# ================================================================= #
# ViewSets para Listar os Conteúdos de Estudo
# ================================================================= #

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar e visualizar Matérias. A requisição GET para
    /api/subjects/ retorna a lista completa de matérias, com seus
    livros e tópicos aninhados.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class TextbookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar e visualizar Livros Didáticos.
    """
    queryset = Textbook.objects.all()
    serializer_class = TextbookSerializer
    permission_classes = [permissions.IsAuthenticated]


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Esta view é o ponto central da trilha. Ao buscar um tópico,
    o serializer calcula o status (bloqueado/desbloqueado) de cada
    quiz para o usuário que fez a requisição.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        """
        Passa o objeto 'request' para o contexto do serializer.
        Isto é essencial para que o QuizSerializer possa acessar
        o request.user e determinar o status de cada quiz.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


# ================================================================= #
# Views para a Lógica Principal de Quiz e Exercícios
# ================================================================= #

class QuizQuestionsView(APIView):
    """
    Retorna as 3 questões de um quiz específico, mas somente se ele
    estiver desbloqueado para o usuário.
    Acessada via GET /api/quizzes/{quiz_id}/questions/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"detail": "Questionário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Lógica para verificar se o quiz está desbloqueado
        is_unlocked = False
        if quiz.level == 1:
            is_unlocked = True
        else:
            try:
                previous_quiz = Quiz.objects.get(topic=quiz.topic, level=quiz.level - 1)
                score = UserQuizScore.objects.get(user=request.user, quiz=previous_quiz)
                if score.score >= previous_quiz.passing_score:
                    is_unlocked = True
            except (Quiz.DoesNotExist, UserQuizScore.DoesNotExist):
                is_unlocked = False

        if not is_unlocked:
            return Response({"detail": "Este questionário está bloqueado."}, status=status.HTTP_403_FORBIDDEN)

        # Retorna as 3 primeiras questões associadas ao quiz
        questions = Question.objects.filter(quiz=quiz)[:3]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class SubmitQuizView(APIView):
    """
    Recebe as respostas de um quiz, calcula a pontuação, salva o resultado
    e retorna o feedback para o usuário.
    Acessada via POST /api/quizzes/{quiz_id}/submit/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"detail": "Questionário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        answers = request.data.get('answers', [])

        questions_in_quiz = Question.objects.filter(quiz=quiz)
        question_map = {q.id: q.correct_answer for q in questions_in_quiz}

        if len(answers) != questions_in_quiz.count() or not answers:
            return Response({"detail": "É necessário responder todas as questões."}, status=status.HTTP_400_BAD_REQUEST)

        correct_count = 0
        for answer in answers:
            question_id = answer.get('question_id')
            submitted = answer.get('submitted_answer')
            if question_id in question_map and question_map[question_id].upper() == submitted.upper():
                correct_count += 1

        # Calcula a pontuação de 0 a 100
        score = round((correct_count / len(questions_in_quiz)) * 100)

        # Salva ou atualiza a melhor pontuação do usuário para este quiz
        score_obj, created = UserQuizScore.objects.get_or_create(user=user, quiz=quiz, defaults={'score': score})
        if not created and score > score_obj.score:
            score_obj.score = score
            score_obj.save()

        # Atualiza a atividade diária do usuário
        activity, _ = UserActivity.objects.get_or_create(user=user, date=timezone.now().date())
        activity.questions_solved += len(questions_in_quiz)
        activity.save()

        return Response({
            "detail": "Questionário finalizado!",
            "your_score": score,
            "passing_score": quiz.passing_score,
            "passed": score >= quiz.passing_score,
        }, status=status.HTTP_200_OK)


# ================================================================= #
# Views do Painel do Usuário (Dashboard, Histórico e Perfil)
# ================================================================= #

class UserDashboardView(APIView):
    """
    Fornece um resumo completo do status do usuário para o painel principal.
    Inclui o streak de estudos e o progresso da meta diária.
    Acessada via GET em /api/dashboard/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        today = timezone.now().date()

        # Cálculo do Streak
        streak = 0
        activities = UserActivity.objects.filter(user=user).order_by('-date')
        if activities.exists():
            last_activity_date = activities.first().date
            if last_activity_date >= today - timedelta(days=1):
                streak_date = last_activity_date
                while any(a.date == streak_date for a in activities):
                    streak += 1
                    streak_date -= timedelta(days=1)

        # Progresso da Meta Diária
        profile, _ = UserProfile.objects.get_or_create(user=user)
        activity_today, _ = UserActivity.objects.get_or_create(user=user, date=today)

        dashboard_data = {
            "username": user.username,
            "streak": streak,
            "daily_goal": profile.daily_goal,
            "questions_solved_today": activity_today.questions_solved
        }

        return Response(dashboard_data, status=status.HTTP_200_OK)


class UserHistoryView(generics.ListAPIView):
    """
    Retorna o histórico de atividades diárias do usuário.
    Acessada via GET em /api/history/
    """
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas as atividades do usuário logado, da mais recente para a mais antiga
        return UserActivity.objects.filter(user=self.request.user).order_by('-date')


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Permite ao usuário visualizar e atualizar seu perfil (ex: meta diária).
    Acessada via GET (para ver) ou PUT/PATCH (para atualizar) em /api/profile/
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retorna o perfil associado ao usuário logado
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile