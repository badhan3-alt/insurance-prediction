import os
import joblib
import pandas as pd

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PredictionSerializer


# =========================================================
# Load ML Model and Scaler
# =========================================================

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "ml",
    "insurance_model.pkl"
)

SCALER_PATH = os.path.join(
    settings.BASE_DIR,
    "ml",
    "scaler.pkl"
)

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


# =========================================================
# Frontend
# =========================================================

def home(request):
    return render(
        request,
        "predictor/index.html"
    )


# =========================================================
# ML Prediction API
# =========================================================

@csrf_exempt
@api_view(["POST"])
def predict_insurance(request):

    # Validate input
    serializer = PredictionSerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=400
        )

    data = serializer.validated_data

    # -----------------------------------------------------
    # Get user input
    # -----------------------------------------------------

    age = data["age"]
    sex = data["sex"]
    bmi = data["bmi"]
    children = data["children"]
    smoker = data["smoker"]
    region = data["region"]


    # -----------------------------------------------------
    # Encode categorical values
    # -----------------------------------------------------

    is_female = 1 if sex == "female" else 0

    is_smoker = 1 if smoker == "yes" else 0

    region_southeast = (
        1 if region == "southeast" else 0
    )

    # BMI category
    bmi_category_obese = (
        1 if bmi >= 30 else 0
    )


    # -----------------------------------------------------
    # Create DataFrame
    # -----------------------------------------------------

    input_data = pd.DataFrame([
        {
            "age": age,
            "is_female": is_female,
            "bmi": bmi,
            "children": children,
            "is_smoker": is_smoker,
            "region_southeast": region_southeast,
            "bmi_category_Obese": bmi_category_obese
        }
    ])


    # -----------------------------------------------------
    # Scale numerical features
    # -----------------------------------------------------

    scale_columns = [
        "age",
        "bmi",
        "children"
    ]

    input_data[scale_columns] = scaler.transform(
        input_data[scale_columns]
    )


    # -----------------------------------------------------
    # Make prediction
    # -----------------------------------------------------

    prediction = model.predict(
        input_data
    )[0]


    # -----------------------------------------------------
    # Return JSON response
    # -----------------------------------------------------

    return Response({
        "success": True,
        "predicted_charge": round(
            float(prediction),
            2
        )
    })