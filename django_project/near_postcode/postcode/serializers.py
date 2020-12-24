from rest_framework import serializers
from .models import Postcode, Coordinate


class PostcodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Postcode
        fields = '__all__'


class CoordinateSerializer(serializers.ModelSerializer):
    postcodes = serializers.PrimaryKeyRelatedField(
        queryset=Postcode.objects.all(), many=True
    )

    class Meta:
        model = Coordinate
        fields = '__all__'

    def create(self, validated_data):
        postcodes = validated_data.pop('postcodes')
        coordinate = Coordinate.objects.create(**validated_data)
        for postcode in postcodes:
            coordinate.postcodes.add(postcode)

        return coordinate
