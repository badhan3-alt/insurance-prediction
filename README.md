# Medical Insurance Cost Predictor

This project turns the supplied `insurance.ipynb` machine-learning work into a Django web application.

## What is included

- Django backend
- HTML/CSS frontend
- Linear Regression insurance-charge prediction
- Reproducible training script
- Saved model and scaler artifacts
- Original `insurance.csv`
- Original `insurance.ipynb`
- Basic Django tests

## Model inputs

The web form accepts:

- Age
- Gender
- BMI
- Number of children
- Smoker status
- Region

The backend transforms those fields into the seven final features used in the notebook:

1. `age`
2. `is_female`
3. `bmi`
4. `children`
5. `is_smoker`
6. `region_southeast`
7. `bmi_category_Obese`

The training script intentionally reproduces the notebook's integer conversion before BMI category creation and standardisation, so the Django inference pipeline matches the notebook.

## Run the project

### 1. Open a terminal in this folder

```bash
cd insurance_django_fullstack
```

### 2. Create a virtual environment (recommended)

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Train/save the model

Saved artifacts are already included, but you can regenerate them at any time:

```bash
python train_model.py
```

### 5. Prepare Django

```bash
python manage.py migrate
```

### 6. Start the website

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Test it

```bash
python manage.py test
```

## Main files

- `train_model.py` — reproduces the notebook preprocessing and trains the model
- `predictor/ml_service.py` — converts form data and calls the model
- `predictor/views.py` — Django request/response logic
- `predictor/forms.py` — validated form fields
- `predictor/templates/predictor/index.html` — frontend page
- `predictor/static/predictor/style.css` — styling
- `ml/artifacts/insurance_model.pkl` — trained model
- `ml/artifacts/scaler.pkl` — fitted scaler
