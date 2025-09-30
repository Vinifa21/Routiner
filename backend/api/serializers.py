# api/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Subject, Textbook, Topic, Quiz, Question, UserQuizScore,
    UserProfile, UserActivity
)


# ================================================================= #
# Serializers para a Lógica de Quiz e Exercícios
# ================================================================= #

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer para as Questões.
    A resposta correta ('correct_answer') é definida como 'write_only',
    o que significa que ela não será enviada nas respostas da API,
    protegendo o gabarito.
    """
    correct_answer = serializers.CharField(write_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'quiz',  # Alterado de 'topic' para 'quiz'
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_answer'
        ]


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer para um Quiz (Questionário).
    Este é o serializer mais complexo, pois ele calcula dinamicamente
    o status ('locked', 'unlocked', 'completed') e a melhor pontuação
    do usuário logado para cada quiz.
    """
    status = serializers.SerializerMethodField()
    user_best_score = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'level', 'status', 'user_best_score']

    def get_user_best_score(self, obj):
        """
        Busca no banco de dados a melhor pontuação do usuário para este quiz.
        Retorna None se o usuário nunca completou este quiz.
        """
        # Acessa o usuário logado a partir do contexto passado pela View
        user = self.context['request'].user
        try:
            score_obj = UserQuizScore.objects.get(user=user, quiz=obj)
            return score_obj.score
        except UserQuizScore.DoesNotExist:
            return None

    def get_status(self, obj):
        """
        Determina e retorna o status do quiz para o usuário logado.
        A lógica de desbloqueio da trilha é implementada aqui.
        """
        user = self.context['request'].user
        best_score = self.get_user_best_score(obj)

        # Se o usuário já passou no quiz, ele está completo.
        if best_score is not None and best_score >= obj.passing_score:
            return 'completed'

        # O primeiro nível (level 1) está sempre desbloqueado.
        if obj.level == 1:
            return 'unlocked'

        # Para desbloquear os níveis seguintes, o usuário precisa ter passado no anterior.
        try:
            previous_quiz = Quiz.objects.get(topic=obj.topic, level=obj.level - 1)
            previous_score_obj = UserQuizScore.objects.get(user=user, quiz=previous_quiz)
            if previous_score_obj.score >= previous_quiz.passing_score:
                return 'unlocked'
        except (Quiz.DoesNotExist, UserQuizScore.DoesNotExist):
            # Se o quiz anterior não existe ou não foi completado, este está bloqueado.
            return 'locked'

        return 'locked'


# ================================================================= #
# Serializers para a Hierarquia de Conteúdo
# ================================================================= #

class TopicSerializer(serializers.ModelSerializer):
    """
    O Serializer de Tópico agora aninha a sua trilha de quizzes,
    usando o QuizSerializer para exibir o status de cada um.
    """
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'textbook', 'quizzes']


class TextbookSerializer(serializers.ModelSerializer):
    """Aninha os Tópicos dentro de cada Livro Didático."""
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Textbook
        fields = ['id', 'title', 'subject', 'topics']


class SubjectSerializer(serializers.ModelSerializer):
    """Aninha os Livros Didáticos dentro de cada Matéria."""
    textbooks = TextbookSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'textbooks']


# ================================================================= #
# Serializers para Dados do Usuário (Perfil, Histórico, etc.)
# ================================================================= #

class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para exibir informações públicas do usuário."""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para o perfil do usuário, usado para gerenciar a meta diária."""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'daily_goal']


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer para o histórico de atividades diárias."""

    class Meta:
        model = UserActivity
        fields = ['date', 'questions_solved']