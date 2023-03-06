from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "role": {"required": False},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context["request"].user
        if not user.is_authenticated and "password" not in attrs:
            raise serializers.ValidationError({"password": "Password is required"})
        return attrs

    def validate_email(self, value):
        if self.instance and self.instance.email != value:
            raise serializers.ValidationError({"email": "Email cannot be changed"})
        return value

    def validate_role(self, value):
        user = self.context["request"].user
        error = serializers.ValidationError(
            {"role": "You don't have permission to assign this role"}
        )

        if value == User.CLIENT:
            return value
        elif not user.is_authenticated:
            raise error
        elif user.role not in User.MANAGER_ROLES:
            raise error
        elif user.role == User.MANAGER and value not in User.EMPLOYEE_ROLES:
            raise error
        return value

    def validate_password(self, value):
        if self.instance:
            raise serializers.ValidationError(
                {"password": "Password cannot be changed"}
            )
        return value

    def create(self, validated_data):
        password = None
        if "password" in validated_data:
            password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)


class EmployeeSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def update(self, user, validated_data):
        user.first_name = validated_data["first_name"]
        user.last_name = validated_data["last_name"]
        user.is_active = True
        user.set_password(validated_data["password"])
        user.save()
        return user
