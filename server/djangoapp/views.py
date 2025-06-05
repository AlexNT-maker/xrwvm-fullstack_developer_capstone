from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
import json

from .models import CarMake, CarModel
from .populate import initiate

# Logger setup
logger = logging.getLogger(__name__)


# ---------- LOGIN ----------
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    response = {"userName": username}
    if user is not None:
        login(request, user)
        response["status"] = "Authenticated"
    else:
        response["status"] = "Failed"
    return JsonResponse(response)


# ---------- LOGOUT ----------
@csrf_exempt
def logout_request(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})


# ---------- REGISTRATION ----------
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": "User already exists"})
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return JsonResponse({"status": "User created"})


# ---------- GET CARS ----------
def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('make')
    cars = [{"CarModel": c.name, "CarMake": c.make.name} for c in car_models]
    return JsonResponse({"CarModels": cars})

