from rest_framework import serializers
from django.contrib.auth.hashers import check_password, make_password
from Invent.models import Items, User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    #Serializer for User creation.

    class Meta:
        model = User
        fields = ['email','password']

    def create(self, validated_data):
        new_password = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        user.password = new_password
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    #Serializer for User login.

    email = serializers.EmailField()
    password = serializers.CharField(max_length=500)

    class Meta:
        model = User
        # fields = ['email', 'password']
        fields = '__all__'

    def to_representation(self, instance):
        response = super(LoginSerializer, self).to_representation(instance)
        response['token'] = instance.auth_token.key
        return response

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data['email'].lower())
        if not user.exists():
            raise serializers.ValidationError({'data': 'Email id does not exist'})
        if not check_password(validated_data['password'], user.first().password):
            raise serializers.ValidationError({'Error': 'Wrong Password'})
        Token.objects.get_or_create(user=user.first())
        return user.first()


class CreateItemSerializer(serializers.ModelSerializer):
    #Serializer to create Item.

    itemName = serializers.CharField(required=False, max_length=100) 
    Price = serializers.FloatField(required=False)

    class Meta:
        model = Items
        exclude = ['user', 'id']

    def create(self, validated_data):
        user =  self.context.user
        validated_data.update({'user':user})
        return Items.objects.create(**validated_data)


class ListSerializer(serializers.ModelSerializer):
    #Serializer to list all items.

    class Meta:
        model = Items
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    # Serializer for all Item operations.
    
    class Meta:
        model = Items
        fields = '__all__'