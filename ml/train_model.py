import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


# =========================================================
# 1. LOAD DATA
# =========================================================

df = pd.read_csv("ml/insurance.csv")


# =========================================================
# 2. DATA CLEANING
# =========================================================

df_cleaned = df.copy()

# Remove duplicates
df_cleaned.drop_duplicates(inplace=True)

# Encode sex
df_cleaned["sex"] = df_cleaned["sex"].map({
    "male": 0,
    "female": 1
})

# Encode smoker
df_cleaned["smoker"] = df_cleaned["smoker"].map({
    "no": 0,
    "yes": 1
})

# Rename columns
df_cleaned.rename(
    columns={
        "sex": "is_female",
        "smoker": "is_smoker"
    },
    inplace=True
)


# =========================================================
# 3. REGION ENCODING
# =========================================================

df_cleaned = pd.get_dummies(
    df_cleaned,
    columns=["region"],
    drop_first=True
)


# =========================================================
# 4. FEATURE ENGINEERING
# =========================================================

df_cleaned["bmi_category"] = pd.cut(
    df_cleaned["bmi"],
    bins=[0, 18.5, 24.9, 29.9, float("inf")],
    labels=[
        "Underweight",
        "Normal",
        "Overweight",
        "Obese"
    ]
)

df_cleaned = pd.get_dummies(
    df_cleaned,
    columns=["bmi_category"],
    drop_first=True
)


# Make sure required columns exist
required_columns = [
    "region_southeast",
    "bmi_category_Obese"
]

for column in required_columns:
    if column not in df_cleaned.columns:
        df_cleaned[column] = 0


# =========================================================
# 5. SELECT FEATURES
# =========================================================

features = [
    "age",
    "is_female",
    "bmi",
    "children",
    "is_smoker",
    "region_southeast",
    "bmi_category_Obese"
]

X = df_cleaned[features]
y = df_cleaned["charges"]


# =========================================================
# 6. TRAIN TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.33,
    random_state=42
)


# =========================================================
# 7. SCALE NUMERICAL FEATURES
# =========================================================

scale_columns = [
    "age",
    "bmi",
    "children"
]

scaler = StandardScaler()

X_train = X_train.copy()
X_test = X_test.copy()

X_train[scale_columns] = scaler.fit_transform(
    X_train[scale_columns]
)

X_test[scale_columns] = scaler.transform(
    X_test[scale_columns]
)


# =========================================================
# 8. TRAIN MODEL
# =========================================================

model = LinearRegression()

model.fit(X_train, y_train)


# =========================================================
# 9. PREDICTION
# =========================================================

y_pred = model.predict(X_test)


# =========================================================
# 10. MODEL EVALUATION
# =========================================================

r2 = r2_score(y_test, y_pred)

n = X_test.shape[0]
p = X_test.shape[1]

adjusted_r2 = (
    1 - (1 - r2) * (n - 1) / (n - p - 1)
)

mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = mse ** 0.5


print("--------------------------------")
print("MODEL PERFORMANCE")
print("--------------------------------")

print(f"R2 Score      : {r2:.4f}")
print(f"Adjusted R2   : {adjusted_r2:.4f}")
print(f"MAE           : {mae:.2f}")
print(f"RMSE          : {rmse:.2f}")


# =========================================================
# 11. SAVE MODEL
# =========================================================

joblib.dump(
    model,
    "ml/insurance_model.pkl"
)

joblib.dump(
    scaler,
    "ml/scaler.pkl"
)

print("--------------------------------")
print("Model saved successfully!")
print("--------------------------------")