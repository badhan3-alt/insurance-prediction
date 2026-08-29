from rest_framework import serializers


class PredictionSerializer(serializers.Serializer):

    age = serializers.IntegerField(min_value=1)
    sex = serializers.ChoiceField(
        choices=["male", "female"]
    )
    bmi = serializers.FloatField(min_value=0)
    children = serializers.IntegerField(min_value=0)
    smoker = serializers.ChoiceField(
        choices=["yes", "no"]
    )
    region = serializers.ChoiceField(
        choices=[
            "southwest",
            "southeast",
            "northwest",
            "northeast"
        ]
    )