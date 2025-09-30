# api/models.py
from django.db import models
from django.contrib.auth.models import User

# --- Modelos de Conteúdo (permanecem os mesmos) ---
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class Textbook(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='textbooks')
    def __str__(self): return f"{self.title} ({self.subject.name})"

class Topic(models.Model):
    name = models.CharField(max_length=100)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, related_name='topics')
    def __str__(self): return f"{self.name} - {self.textbook.title}"

# --- NOVOS Modelos para a Lógica da Trilha ---

class Quiz(models.Model):
    """Representa um questionário (um 'nível') dentro de um tópico."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    level = models.PositiveIntegerField(help_text="A ordem do quiz na trilha (1, 2, 3...)")
    passing_score = models.PositiveIntegerField(default=80, help_text="Pontuação mínima (de 100) para desbloquear o próximo quiz")

    class Meta:
        ordering = ['level'] # Garante que os quizzes sempre sejam ordenados por nível
        unique_together = ('topic', 'level')

    def __str__(self):
        return f"Nível {self.level}: {self.title} ({self.topic.name})"

class Question(models.Model):
    """Uma questão agora pertence a um Quiz específico, não a um Tópico."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions') # MUDANÇA AQUI
    question_text = models.TextField()
    # Opções e resposta correta permanecem iguais...
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return self.question_text[:50]

# --- NOVOS Modelos de Progresso do Usuário ---

class UserQuizScore(models.Model):
    """Armazena a melhor pontuação de um usuário em um quiz específico."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField() # A melhor pontuação do usuário (0 a 100)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'quiz')

# --- Modelos de Perfil e Atividade (permanecem os mesmos) ---
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_goal = models.PositiveIntegerField(default=5)
    def __str__(self): return self.user.username

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    questions_solved = models.PositiveIntegerField(default=0)
    class Meta:
        unique_together = ('user', 'date')