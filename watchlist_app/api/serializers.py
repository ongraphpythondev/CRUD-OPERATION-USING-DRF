from django.forms import ValidationError
from rest_framework import serializers

from watchlist_app.models import WatchList, StreamPlatForm, Reviews

# Model Serializers


class ReviewSerializers(serializers.ModelSerializer):

    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reviews
        #fields = '__all__'
        exclude = ('watchlist',)


class WatchListSerializers(serializers.ModelSerializer):

    #reviews = ReviewSerializers(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = '__all__'
        # exclude = ['is_active']


class StreamPlatformSerializers(serializers.ModelSerializer):

    #watchlist = WatchListSerializers(many=True, read_only=True)
    watchlist = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='watch-detail'
    )
    #watchlist = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = StreamPlatForm
        fields = '__all__'

# Serializers class

# class MovieSerializers(serializers.Serializer):

#     def name_len(self, value):
#         if len(value)<2:
#             raise serializers.ValidationError("Name is too short")
#         else:
#             return value

#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_len])
#     description = serializers.CharField()
#     is_active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.is_active = validated_data.get('is_active', instance.is_active)
#         instance.save()
#         return instance

    # field level validation
    # def validate_name(self, value):
    #     if(len(value)<2):
    #         raise serializers.ValidationError("Name is Too Short")
    #     else:
    #         return value
