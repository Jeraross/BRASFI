from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    TIPO_USUARIO = (
        ('mentor', 'Mentor'),
        ('aprendiz', 'Aprendiz'),
    )

    profilePic = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    userType = models.CharField(max_length=10, choices=TIPO_USUARIO, default='aprendiz')

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profilePic": self.profilePic.url if self.profilePic else None,
            "userType": self.userType,
        }

def video_upload_path(instance, filename):
    return f'videos/user_{instance.user.id}/{timezone.now().strftime("%Y%m%d%H%M%S")}_{filename}'

def thumbnail_upload_path(instance, filename):
    return f'video_thumbnails/user_{instance.user.id}/{filename}'

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to=video_upload_path)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'video_file': self.video_file.url if self.video_file else None,
            'created_at': self.created_at.isoformat(),
            'user': self.user.username,
        }
    
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes", null=True, blank=True)
    time_per_question = models.IntegerField(default=20)  # << NOVO

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text 
    
class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    score = models.IntegerField()
    total = models.IntegerField()
    percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'user')  # impede refazer o mesmo quiz

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}: {self.percentage}%"
    
class Projeto(models.Model):
    AREA_IMPACTO_CHOICES = [
        ("educacao", "Educação"),
        ("meio_ambiente", "Meio Ambiente"),
        ("saude", "Saúde"),
        ("tecnologia", "Tecnologia"),
        ("outros", "Outros"),
    ]

    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("aprovado", "Aprovado"),
        ("rejeitado", "Rejeitado"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    impact_area = models.CharField(max_length=30, choices=AREA_IMPACTO_CHOICES)
    objective = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projetos")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")
    created_at = models.DateTimeField(default=timezone.now)
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'impact_area': self.get_impact_area_display(),
            'objective': self.objective,
            'status': self.get_status_display(),
            'created_at': self.created_at.isoformat(),
            'user': self.user.username,
            'rejection_reason': self.rejection_reason,
        }

class TopicConversa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo
    
    def serialize(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'user': self.user.username,
            'created_at': self.created_at.isoformat(),
        }

class Comentario(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.username} comentou em {self.projeto.title}"

class Resposta(models.Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name="respostas")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.username} respondeu a {self.comentario.id}"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'projeto')  # Um usuário só pode dar 1 like por projeto