import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import joblib
from sklearn.metrics import r2_score
# 1. Load data
data = pd.read_csv('crop_yield.csv')

# 2. Clean all text columns
for col in data.select_dtypes(include='object').columns:
    data[col] = data[col].str.strip()


# 2. Calculate Yield (Production per Area)
data['Yield'] = data['Production'] / data['Area']

# 3. Prepare features and target
X = data.drop(['Yield', 'Crop_Year'], axis=1)  # Drop Crop_Year if not needed
y = data['Yield']

# 4. Encode categorical columns
label_encoders = {}

for column in X.columns:
    if X[column].dtype == 'object':
        le = LabelEncoder()
        X[column] = le.fit_transform(X[column])
        label_encoders[column] = le

# 5. Save available values for each category
available_values = {
    'Crop': list(label_encoders['Crop'].classes_),
    'Season': list(label_encoders['Season'].classes_),
    'State': list(label_encoders['State'].classes_),
}

# 6. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 8. Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Test Mean Squared Error: {mse}")

# 9. Save model, encoders, and available values
joblib.dump((model, label_encoders, available_values), 'crop_yield_model.pkl')

print("✅ Model, encoders, and available values saved as 'crop_yield_model.pkl'")
