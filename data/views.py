from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Crop, Season, State, Prediction
import joblib
import os
import pandas as pd
import numpy as np
from django.contrib import messages
from django.db.models import Q

# Model loading
import joblib

# Load the trained model, encoders, and available values
model, label_encoders, available_values = joblib.load('ml_model/crop_yield_model.pkl')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password')
        return render(request, 'login.html')

    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('login')

    return render(request, 'register.html')




@login_required
def home_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        # 1. Get form inputs
        test_crop = request.POST.get('crop')
        test_season = request.POST.get('season')
        test_state = request.POST.get('state')

        try:
            test_area = float(request.POST.get('area'))
            test_production = float(request.POST.get('production'))
            test_annual_rainfall = float(request.POST.get('annual_rainfall'))
            test_fertilizer = float(request.POST.get('fertilizer'))
            test_pesticide = float(request.POST.get('pesticide'))
        except ValueError:
            return render(request, 'home.html', {'error': 'Please enter valid numerical values!'})

        # 2. Validate text inputs
        if test_crop not in available_values['Crop']:
            return render(request, 'home.html', {'error': f'Invalid Crop selected. Available options: {available_values["Crop"]}'})
        if test_season not in available_values['Season']:
            return render(request, 'home.html', {'error': f'Invalid Season selected. Available options: {available_values["Season"]}'})
        if test_state not in available_values['State']:
            return render(request, 'home.html', {'error': f'Invalid State selected. Available options: {available_values["State"]}'})

        # 3. Encode categorical variables
        crop_encoded = label_encoders['Crop'].transform([test_crop])[0]
        season_encoded = label_encoders['Season'].transform([test_season])[0]
        state_encoded = label_encoders['State'].transform([test_state])[0]

        # 4. Prepare DataFrame for prediction
        input_dict = {
            'Crop': [crop_encoded],
            'Season': [season_encoded],
            'State': [state_encoded],
            'Area': [test_area],
            'Production': [test_production],
            'Annual_Rainfall': [test_annual_rainfall],
            'Fertilizer': [test_fertilizer],
            'Pesticide': [test_pesticide]
        }
        input_df = pd.DataFrame(input_dict)

        # 5. Predict
        predicted_yield = model.predict(input_df)[0]

        return render(request, 'home.html', {'result': f"Predicted Yield: {predicted_yield:.2f} tons per hectare"})

    return render(request, 'home.html')

def logout_user(request):
    logout(request)
    return redirect('login')