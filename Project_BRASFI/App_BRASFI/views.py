from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg, Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Video, Quiz, Question, Choice, QuizResult, Projeto, Comentario, Resposta, Like
from django.http import JsonResponse
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@csrf_exempt
def sugerir_desafios(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            area = data.get('impact_area')
            title = data.get('title')
            description = data.get('description')


            if not area:
                return JsonResponse({'error': 'Área de impacto não fornecida.'}, status=400)

            prompt = f"me diga de forma objetiva três desafios estratégicos comuns na área de impacto '{area}' que podem inspirar projetos inovadores?"


            model = genai.GenerativeModel("gemini-2.0-flash-001")
            response = model.generate_content(prompt)

            texto = response.text.strip()
            sugestoes = [
                linha.strip("-•1234567890. ").strip()
                for linha in texto.split("\n")
                if linha.strip()
            ]

            return JsonResponse({'sugestoes': sugestoes})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def solicitar_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get("title", "").strip()
            description = data.get("description", "").strip()
            impact_area = data.get("impact_area", "").strip()
            objective = data.get("objective", "").strip()

            # Verificação dos campos obrigatórios
            if not all([title, description, impact_area, objective]):
                return JsonResponse({
                    'error': 'Por favor, preencha todos os campos obrigatórios antes de solicitar feedback.'
                }, status=400)

            # Prompt para a IA
            prompt = (
                f"quero uma resposta objetiva: Sou um assistente de inovação. Analise este projeto e forneça sugestões de melhoria:\n\n"
                f"Título: {title}\n"
                f"Descrição: {description}\n"
                f"Área de Impacto: {impact_area}\n"
                f"Objetivo: {objective}\n\n"
                f"Com base nessas informações, sugira melhorias claras e construtivas para aumentar as chances de sucesso do projeto."
            )

            model = genai.GenerativeModel("gemini-2.0-flash-001")
            response = model.generate_content(prompt)

            texto = response.text.strip()
            sugestoes = [
                linha.strip("-•1234567890. ").strip()
                for linha in texto.split("\n")
                if linha.strip()
            ]

            return JsonResponse({'feedback': sugestoes})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)


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
def EditProfileView(request):
    if request.method == 'POST':
        user = request.user

        new_username = request.POST.get('username', user.username).strip()
        profile_pic = request.FILES.get('profilePic') 

        if new_username != user.username and User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
            messages.error(request, 'Este nome de usuário já está em uso. Escolha outro.')
            return HttpResponseRedirect(reverse("App_BRASFI:projecthub"))

        user.username = new_username
        user.save()

        if profile_pic:
            profile = getattr(user, 'profile', None)
            if profile:
                profile.profilePic = profile_pic
                profile.save()

        messages.success(request, 'Perfil atualizado com sucesso!')
        return HttpResponseRedirect(reverse("App_BRASFI:projecthub"))

    return HttpResponse("Method must be 'POST'")

@login_required
def ProjectHubView(request):
    projetos = Projeto.objects.filter(status="aprovado").order_by("-created_at")

    liked_ids = set(
        Like.objects.filter(user=request.user)
                    .values_list('projeto_id', flat=True)
    )

    return render(request, "projecthub.html", {
        "page": "projecthub",
        "projetos": projetos,
        "liked_projects": liked_ids 
    })

@login_required
def CuradoriaView(request):
    projetos = Projeto.objects.filter(status="pendente").order_by("-created_at")
    return render(request, "curadoria.html", {
        "page": "curadoria",
        "projetos": projetos
    })

@login_required
def CreateProjectView(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        impact_area = request.POST.get("impact_area")
        objective = request.POST.get("objective")

        if title and description and impact_area and objective:
            try:
                with transaction.atomic():
                    Projeto.objects.create(
                        title=title,
                        description=description,
                        impact_area=impact_area,
                        objective=objective,
                        user=request.user
                    )
                messages.success(request, "Projeto enviado para análise!")
                return HttpResponseRedirect(reverse('App_BRASFI:projecthub'))
            except IntegrityError:
                messages.error(request, "Erro ao cadastrar o projeto.")
                return HttpResponseRedirect(reverse('App_BRASFI:projecthub'))
        else:
            messages.error(request, "Todos os campos são obrigatórios.")
            return HttpResponseRedirect(reverse('App_BRASFI:projecthub'))
    else:
        return HttpResponse("Method must be 'POST'")

@require_POST
@login_required
def aprovar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if projeto.status != "aprovado":
        projeto.status = "aprovado"
        projeto.rejection_reason = None  # Limpa a rejeição anterior, se houver
        projeto.save()
        messages.success(request, "Projeto aprovado com sucesso!")
    else:
        messages.info(request, "O projeto já está aprovado.")

    return redirect('App_BRASFI:projecthub')


@require_POST
@login_required
def rejeitar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    rejection_reason = request.POST.get("rejection_reason", "").strip()

    if not rejection_reason:
        messages.error(request, "Por favor, forneça um motivo para a rejeição.")
        return redirect('App_BRASFI:projecthub')

    projeto.status = "rejeitado"
    projeto.rejection_reason = rejection_reason
    projeto.save()

    # Envia o e-mail para o dono do projeto
    try:
        email_html = render_to_string(
            'emails/rejeicao_projeto.html',
            {
                'usuario': projeto.user,
                'projeto': projeto,
                'motivo': rejection_reason
            }
        )

        send_mail(
            subject='Seu projeto foi rejeitado',
            message='',  # Texto simples pode ser vazio
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[projeto.user.email],
            html_message=email_html,
            fail_silently=False
        )
        messages.success(request, "Projeto rejeitado com sucesso e e-mail enviado!")

    except Exception as e:
        messages.warning(request, f"Projeto rejeitado, mas houve um erro ao enviar o e-mail: {str(e)}")

    return redirect('App_BRASFI:projecthub')

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


    return render(request, "videos.html", {
        "page": "videos",
        "videos": all_videos,
        'top_mentors': top_mentors_raw,
    })

@login_required
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

@login_required
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

    user_stats = {}
    top_students = []

    if request.user.userType == 'aprendiz':
        results = QuizResult.objects.filter(user=request.user)
        total = results.count()
        avg = results.aggregate(Avg('percentage'))['percentage__avg'] or 0
        best = results.order_by('-percentage').first()

        user_stats = {
            'total_quizzes': total,
            'average_score': round(avg, 2),
            'best_score': best.percentage if best else 0,
            'best_quiz': best.quiz.title if best else None
        }

    elif request.user.userType == 'mentor':
        # Alunos com mais de 1 quiz feito e boa média
        top_students = (
            QuizResult.objects
            .values('user__username', 'user__profilePic')
            .annotate(
                total_quizzes=Count('quiz', distinct=True),
                avg_score=Avg('percentage')
            )
            .filter(total_quizzes__gte=1)
            .order_by('-avg_score')[:5]
        )

    return render(request, "quizzes.html", {
        "page": "quizzes",
        "quizzes_with_ranking": quizzes_with_ranking,
        "user_stats": user_stats,
        "top_students": top_students
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


def forum_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    comentarios = Comentario.objects.filter(projeto=projeto).order_by('-criado_em')
    return render(request, 'forum.html', {'projeto': projeto, 'comentarios': comentarios})

@login_required
def novo_comentario(request, projeto_id):
    if request.method == 'POST':
        texto = request.POST.get('mensagem', '').strip()
        if texto:
            projeto = get_object_or_404(Projeto, id=projeto_id)
            Comentario.objects.create(projeto=projeto, autor=request.user, mensagem=texto)
        else:
            messages.error(request, "Comentário vazio não permitido.")
    return redirect('App_BRASFI:projecthub')


@login_required
def responder_comentario(request, comentario_id):
    if request.method == 'POST':
        texto = request.POST.get('mensagem', '').strip()
        if texto:
            comentario = get_object_or_404(Comentario, id=comentario_id)
            Resposta.objects.create(comentario=comentario, autor=request.user, mensagem=texto)
        else:
            messages.error(request, "Resposta vazia não permitida.")
    return redirect('App_BRASFI:projecthub')

@login_required
def delete_project(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    # Só o aprendiz dono pode excluir
    if request.user.userType == 'aprendiz' and projeto.user == request.user:
        projeto.delete()
        messages.success(request, "Projeto excluído com sucesso.")
    else:
        messages.error(request, "Você não tem permissão para excluir este projeto.")
    return redirect('App_BRASFI:projecthub')

@login_required
def like_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, projeto=projeto)

    if not created:
        # Se o like já existia, o usuário está removendo o like
        like.delete()
        liked = False
    else:
        liked = True

    total_likes = Like.objects.filter(projeto=projeto).count()
    return JsonResponse({'liked': liked, 'total_likes': total_likes})

@login_required
def curtir_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    # Alterna curtida
    like, created = Like.objects.get_or_create(user=request.user, projeto=projeto)

    if not created:
        # Já existia, remove
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'total_likes': projeto.like_set.count(),
        'liked': liked
    })