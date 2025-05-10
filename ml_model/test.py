# test_model_input.py

import joblib
import numpy as np

# 1. Load model, encoders, and available values
model, label_encoders, available_values = joblib.load('crop_yield_model.pkl')

# 2. Take input from the user
print("📥 Please enter the following details:")

print("\nAvailable Crops:", ', '.join(available_values['Crop']))
test_crop = input("Enter Crop: ")

print("\nAvailable Seasons:", ', '.join(available_values['Season']))
test_season = input("Enter Season: ")

print("\nAvailable States:", ', '.join(available_values['State']))
test_state = input("Enter State: ")

try:
    test_area = float(input("\nEnter Area in hectares (e.g., 2.5): "))
    test_production = float(input("Enter Production in tons (e.g., 5.0): "))
    test_annual_rainfall = float(input("Enter Annual Rainfall in mm (e.g., 800): "))
    test_fertilizer = float(input("Enter Fertilizer used (kg/hectare) (e.g., 150): "))
    test_pesticide = float(input("Enter Pesticide used (kg/hectare) (e.g., 50): "))
except ValueError:
    print("❌ Invalid number entered. Please enter valid numerical values.")
    exit()

# 3. Validate user input
if test_crop not in available_values['Crop']:
    print(f"❌ Invalid Crop. Available Crops: {available_values['Crop']}")
    exit()

if test_season not in available_values['Season']:
    print(f"❌ Invalid Season. Available Seasons: {available_values['Season']}")
    exit()

if test_state not in available_values['State']:
    print(f"❌ Invalid State. Available States: {available_values['State']}")
    exit()

# 4. Encode the categorical features
crop_encoded = label_encoders['Crop'].transform([test_crop])[0]
season_encoded = label_encoders['Season'].transform([test_season])[0]
state_encoded = label_encoders['State'].transform([test_state])[0]

import pandas as pd

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

predicted_yield = model.predict(input_df)[0]


# 7. Output the result
print(f"\n✅ Predicted Yield: {predicted_yield:.2f} tons per hectare 🌾")
