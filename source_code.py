# urls.py
from django.urls import path, include
from todo.views import *

urlpatterns = [
    path('', main_view, name='home'),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', registration_view, name='registration'),
    path('add/', add_view, name="add"),
    path("change/<int:todo_pk>/", change_view, name="change"),
    path("delete/<int:todo_pk>/", delete_view, name="delete")
]



# views.py
from django.shortcuts import render, redirect
from .forms import RegistrationForm, AddForm
from django.contrib.auth.models import User
from .models import ToDo

def registration_view(request):
	if request.method == "GET":
		return render(request, "registration.html", {"registration_form": RegistrationForm()})
	else:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("/auth/login/")
		return render(request, "registration.html", {"registration_form": form})

def main_view(request):
	if request.user.is_authenticated:
		change_forms = []
		for todo in ToDo.objects.filter(user_id=request.user.id):
			form = AddForm({"todo": todo.todo})
			form.id = todo.id
			change_forms.append(form)
		return render(request, "home.html", {"todos": change_forms, "add_form": AddForm()})
	else:
		return render(request, "home.html")

def add_view(request):
	form = AddForm(request.POST)
	todo = form.save()
	todo.user = request.user
	todo.save()
	return redirect("/")

def change_view(request, todo_pk):
	todo = ToDo.objects.get(pk=todo_pk)
	todo.todo = request.POST["todo"]
	todo.save()
	return redirect("/")

def delete_view(request, todo_pk):
	todo = ToDo.objects.get(pk=todo_pk)
	todo.delete()
	return redirect("/")




# login.html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Document</title>
</head>
<body>
	<form method="post">
		{% csrf_token %}
		{{ form.as_p }}
		<button type="submit">Login</button>
	</form>
</body>
</html>	



# home.html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Document</title>
</head>
<body>
	{% if request.user.is_authenticated %}
		Hello {{ user.username }}. <a href="{% url 'logout' %}">Logout</a>
		{% for todo in todos %}
			<form action="change/{{ todo.id }}/" method="post">
				{% csrf_token %}
				{{ todo }}
				<button type="submit">Change</button>
			</form>
			<form action="delete/{{ todo.id }}/" method="post">
				{% csrf_token %}
				<button type='submit'>Delete</button>
			</form>
		{% endfor %}
		<form action="add/" method="post">
			{% csrf_token %}
			{{ add_form.as_p }}
			<button type="submit">Add</button>
		</form>
	{% else %}
		Hello, <a href="{% url 'login' %}">Login</a>, <a href="{% url 'registration' %}">Registration</a>.
	{% endif %}
</body>
</html>



# registration.html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Document</title>
</head>
<body>
	<form method="post">
		{% csrf_token %}
		<div>
			{{ registration_form.errors }}
		</div>
		{{ registration_form.as_p }}
		<input type="submit">
	</form>
</body>
</html>