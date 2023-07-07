from rest_framework import serializers


class AISerializer(serializers.Serializer):
    search = serializers.CharField()

