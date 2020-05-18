from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import login as auth_login
from django.http import HttpResponse

def archive(request):
    return render(request, 'templates/archive.html', {"posts":
                                                          Article.objects.all()})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404


def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'text': request.POST["text"], 'title':
        request.POST["title"]
            }
            if form["text"] and form["title"]:
                post = Article.objects.get(title=form["title"])
                if post.title == form["title"]:
                    form['errors'] = u"Статья с таким названием уже существует"
                    return render(request, 'create_post.html',
                                  {'form': form})
                Article.objects.create(text=form["text"],
        title=form["title"], author=request.user)
                return redirect('get_article',
        article_id=article.id)
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html',
                              {'form': form})
        else:
            return render(request, 'create_post.html', {})
    else:
        raise Http404

def user_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        form = {
            'text': request.POST["text"], 'email':
                request.POST["email"], 'username': request.POST["username"]
        }
        if form["text"] and form["email"] and form["username"]:
            try:
                User.objects.get(username=username)
                form['errors'] = u"Пользователь с таким именем уже есть"
                return render(request, 'signup.html',
                              {'form': form})
            except User.DoesNotExist:
                User.objects.create_user(username, email, password)
                return HttpResponse("Успешная регистрация! Пожалуйста, <a href='/login/'>авторизуйтесь</a>, чтобы начать пользоваться сайтом.")
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'signup.html',
                            {'form': form})

    return render(request, "signup.html", {})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = {
            'password': request.POST["password"], 'username':
                request.POST["username"]
        }
        if form["password"] and form["username"]:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("http://127.0.0.1:8000/")
            else:
                form['errors'] = u"Аккаунт не существует"
                return render(request, 'login.html',
                              {'form': form})
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'login.html',
                            {'form': form})
    else:
        return render(request, 'login.html', {})


















