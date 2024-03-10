from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from openai import OpenAI

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone

openai_api_key = "OPEN_AI_KEY_HERE"
OpenAI.api_key = openai_api_key

client = OpenAI(api_key="OPEN_AI_KEY_HERE")


def ask_openai(message):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": message},
        ],
    )
    # print(completion.choices[0].message.content)
    answer = completion.choices[0].message.content
    return answer


# Create your views here.


def chatbot(request):
    chats = Chat.objects.filter(user = request.user)

    if request.method == "POST":
        message = request.POST.get("message")
        response = ask_openai(message)
        chat = Chat(
            user=request.user,
            message=message,
            response=response,
            created_at=timezone.now(),
        )
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html", {'chats': chats})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("chatbot")
        else:
            error_message = "Invalid username or password ʕ ﾟ ● ﾟʔ"
            return render(request, "login.html", {"error_nessage": error_message})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect("chatbot")
            except:
                error_message = (
                    "Oops, something bad happened. We´ll review the issue ASAP."
                )
                return render(
                    request, "register.html", {"error_message": error_message}
                )
        else:
            error_message = "Passwords do not match"
            return render(request, "register.html", {"error_message": error_message})

    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect("login")
