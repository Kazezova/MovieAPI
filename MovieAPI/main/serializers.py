from rest_framework import serializers
from main.models import Genre, Movie, Score
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class MovieDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     instance.avg_score = validated_data.get('avg_score', instance.avg_score)
    #     instance.save()
    #     return instance


class MovieListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = ('title', 'poster', 'genre', 'country', 'avg_score')


class ScoreSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    movie_id = serializers.IntegerField()
    score = serializers.IntegerField()

    def create(self, validated_data):
        return Score.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user', instance.user_id)
        instance.movie_id = validated_data.get('movie', instance.movie_id)
        instance.score = validated_data.get('score', instance.score)
        instance.save()
        return instance

    def validate(self, data):
        movie_id = data.get('movie_id') or self.instance.movie_id
        obj = Movie.objects.get_movie(pk=movie_id)
        if not obj:
            raise serializers.ValidationError("There is no such movie.")
        else:
            score = data['score']
            if score < 0 or score > 10:
                raise serializers.ValidationError("Invalid movie score.")
        return data
