from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from random import sample
from .models import User, Video, Quiz, Question, Choice, QuizResult
from django.http import JsonResponse
import json


def LandingView(request):
    return render(request, 'landing.html')

def LoginView(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("App_BRASFI:projecthub"))
        else:
            return render(request, "login.html", {
                "message": "Senha ou usuário inválido."
            })
    else:
        return render(request, "login.html")


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("App_BRASFI:landing"))

def RegisterView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        tipo = request.POST.get("tipo")
        profile = request.FILES.get("profile")

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Senhas não coincidem."
            })

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.userType = tipo

            if profile:
                user.profilePic = profile

            user.save()

        except IntegrityError:
            return render(request, "register.html", {
                "message": "Usuário já existe."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("App_BRASFI:projecthub"))

    return render(request, "register.html")


@login_required
def ProjectHubView(request):
    return render(request, "projecthub.html", {
        "page": "projecthub"
    })

@login_required
def NetworkHubView(request):
    return render(request, "networkhub.html", {
        "page": "networkhub"
    })

@login_required
def VideosView(request):
    all_videos = Video.objects.all().order_by('-created_at')

    # Top mentores baseados no número de vídeos
    top_mentors_raw = User.objects.filter(userType="mentor")\
        .annotate(total_videos=Count('videos'))\
        .order_by('-total_videos')[:5]

    # Vídeos recomendados (3 aleatórios)
    recommended_videos = sample(list(all_videos), 3) if all_videos.count() >= 3 else all_videos

    return render(request, "videos.html", {
        "page": "videos",
        "videos": all_videos,
        'top_mentors': top_mentors_raw,
        'recommended_videos': recommended_videos,
    })

def CreateVideoView(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        video_file = request.FILES.get("video_file")

        if title and description and video_file:
            try:
                with transaction.atomic():
                    video = Video.objects.create(
                        title=title,
                        description=description,
                        video_file=video_file,
                        user=request.user
                    )
                    video.save()
                messages.success(request, "Vídeo criado com sucesso!")
                return HttpResponseRedirect(reverse('App_BRASFI:videos'))
            except IntegrityError:
                messages.error(request, "Erro ao criar o vídeo.")
                return HttpResponseRedirect(reverse('App_BRASFI:videos'))
    else:
        return HttpResponse("Method must be 'POST'")


@login_required
def DeleteVideoView(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    # Verifica se o usuário que está tentando excluir é o dono do vídeo
    if video.user == request.user:
        video.delete()
        messages.success(request, "Vídeo excluído com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para excluir este vídeo.")

    return redirect('App_BRASFI:videos')


def QuizzesView(request):
    quizzes = Quiz.objects.all().order_by('-id')
    quizzes_with_ranking = []

    for quiz in quizzes:
        item = {
            'quiz': quiz,
            'user_result': None,
            'ranking': [],
            'has_played': False
        }

        if request.user.userType == 'aprendiz':
            user_result = QuizResult.objects.filter(user=request.user, quiz=quiz).first()
            item['user_result'] = user_result
            item['has_played'] = user_result is not None

        if request.user.userType == 'mentor':
            item['ranking'] = quiz.results.order_by('-percentage')

        quizzes_with_ranking.append(item)

    return render(request, "quizzes.html", {
        "page": "quizzes",
        "quizzes_with_ranking": quizzes_with_ranking
    })



@login_required
def CreateQuizView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        questions = data.get('questions', [])
        time_per_question = data.get('time', 20)  # <- NOVO: tempo por pergunta

        if not title or not questions:
            return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

        try:
            with transaction.atomic():
                quiz = Quiz.objects.create(
                    title=title,
                    description=description,
                    user=request.user,
                    time_per_question=time_per_question  # <- SALVA o tempo no banco
                )

                for q in questions:
                    question = Question.objects.create(quiz=quiz, text=q['text'])
                    for choice in q.get('choices', []):
                        Choice.objects.create(
                            question=question,
                            text=choice.get('text'),
                            is_correct=choice.get('is_correct', False)
                        )

            return JsonResponse({'status': 'ok', 'quiz_id': quiz.id})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@login_required
@csrf_exempt
def DeleteQuizView(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        # Aqui você pode adicionar verificação: só mentor pode deletar
        if request.user.userType != 'mentor':
            return JsonResponse({'error': 'Não autorizado'}, status=403)

        quiz.delete()
        return JsonResponse({'status': 'ok'})

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def PlayQuizView(request, quiz_id):
    if request.user.userType != 'aprendiz':
        return redirect('App_BRASFI:quizzes')

    quiz = get_object_or_404(Quiz, id=quiz_id)

    questions_qs = quiz.questions.prefetch_related('choices').all()

    questions = []
    for q in questions_qs:
        questions.append({
            "id": q.id,
            "text": q.text,
            "choices": [
                {"id": c.id, "text": c.text, "is_correct": c.is_correct}
                for c in q.choices.all()
            ]
        })

    return render(request, 'quiz_play.html', {
        'quiz': quiz,
        'questions': questions,
        'time_per_question': quiz.time_per_question or 20
    })

@login_required
@csrf_exempt
def SubmitQuizResultView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        quiz_id = data.get('quiz_id')
        score = data.get('score')
        total = data.get('total')

        quiz = get_object_or_404(Quiz, id=quiz_id)
        percentage = (score / total) * 100

        QuizResult.objects.update_or_create(
            quiz=quiz,
            user=request.user,
            defaults={
                'score': score,
                'total': total,
                'percentage': percentage
            }
        )

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error', 'message': 'Método inválido'}, status=400)

@login_required
def CuradoriaView(request):
    return render(request, "curadoria.html", {
        "page": "curadoria"
    })

def landing(request):
    return render(request, 'landing.html')
