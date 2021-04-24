from rest_framework import serializers
from auth_.models import MainUser, Profile
from utils.constants import GENDERS, COUNTRIES


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('id', 'user_name', 'email',)


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    gender = ChoiceField(choices=GENDERS)
    country = ChoiceField(choices=COUNTRIES)

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

