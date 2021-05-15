from rest_framework import serializers
from main.models import Genre, Movie, Score, Review, FavoriteWatched, Producer, MPAA


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class MPAASerializer(serializers.ModelSerializer):
    class Meta:
        model = MPAA
        fields = '__all__'


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ('id', 'first_name', 'last_name',)


class ProducerDetailSerializer(ProducerSerializer):
    class Meta(ProducerSerializer.Meta):
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster', 'genre', 'country', 'release_date', 'avg_score', 'cnt_voters')


class MovieDetailSerializer(MovieListSerializer):
    producer = ProducerSerializer()
    rating = MPAASerializer()

    class Meta(MovieListSerializer.Meta):
        fields = '__all__'


class MovieCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


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


class FavoriteWatchedSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer()

    class Meta:
        model = FavoriteWatched
        fields = ('movie',)


class FavoriteWatchedManipulateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    movie_id = serializers.IntegerField()
    favorite = serializers.BooleanField()
    watched = serializers.BooleanField()

    def create(self, validated_data):
        return FavoriteWatched.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user', instance.user_id)
        instance.movie_id = validated_data.get('movie', instance.movie_id)
        instance.favorite = validated_data.get('favorite', instance.favorite)
        instance.watched = validated_data.get('watched', instance.watched)
        instance.save()
        return instance

    def validate(self, data):
        movie_id = data.get('movie_id') or self.instance.movie_id
        obj = Movie.objects.get_movie(pk=movie_id)
        if not obj:
            raise serializers.ValidationError("There is no such movie.")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'author', 'created_date', 'updated_date', 'content',)


class ReviewManipulateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author_id = serializers.IntegerField()
    movie_id = serializers.IntegerField()
    created_date = serializers.DateTimeField(read_only=True)
    updated_date = serializers.DateTimeField(allow_null=True)
    content = serializers.CharField()

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updated_date = validated_data.get('updated_date', instance.updated_date)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    def validate(self, data):
        movie_id = data.get('movie_id') or self.instance.movie_id
        obj = Movie.objects.get_movie(pk=movie_id)
        if not obj:
            raise serializers.ValidationError("There is no such movie.")
        return data


class GenreViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
