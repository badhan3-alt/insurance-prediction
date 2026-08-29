from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'age',
        'sex',
        'bmi',
        'children',
        'smoker',
        'region',
        'predicted_charge',
        'created_at',
    )

    list_filter = ('sex', 'smoker', 'region')
    search_fields = ('sex', 'smoker', 'region')