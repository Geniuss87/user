from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=255,min_length=4)
    password = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    secret_code = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = '__all__'

    def save(self):
        email = self.validated_data['email']
        username = self.validated_data['username']
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'account': 'Account is already exists'})
        else:
            user = User.objects.create(
                username=self.validated_data['username'],
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'],
                email=self.validated_data['email'],
                secret_code=self.validated_data['secret_code']
                )
            password = self.validated_data['password']
            user.is_active = True
            user.set_password(password)
            user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']
        if username and password:
            user = authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    return user
                else:
                    raise serializers.ValidationError({'user': 'User is not active'})
            else:
                raise serializers.ValidationError({'user': 'Please enter valid user credentials'})
        else:
            raise serializers.ValidationError({'error': 'Username and password not to be blank'})


class ResetPasswordSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    secret_code = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = '__all__'

    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']
        secret_code = self.validated_data['secret_code']
        if User.objects.filter(username=username).exists() and User.objects.filter(username=username,
                                                                                   secret_code=secret_code):
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return user
        raise serializers.ValidationError({'error': 'Please enter valid credentials'})
