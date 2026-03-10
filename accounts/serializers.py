from django.contrib.auth.models import User  # Django 기본 User 모델 사용
from rest_framework import serializers  # DRF Serializer 사용


class SignupSerializer(
    serializers.Serializer
):  # 회원가입 요청 데이터를 처리하기 위한 Serializer
    username = serializers.CharField(max_length=150)  # 사용자 아이디
    password = serializers.CharField(
        write_only=True, min_length=4
    )  # 비밀번호 (write_only=True -> 응답 JSON에는 포함되지 않음)
    password2 = serializers.CharField(
        write_only=True, min_length=4
    )  # 비밀번호 확인 입력

    def validate_username(
        self, value
    ):  # username 필드 검증: 같은 username이 이미 존재하는지 확인
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용중인 username 입니다.")
        return value  # 문제가 없으면 username 반환

    def validate(self, attrs):  # 전체 데이터 검증
        if (
            attrs["password"] != attrs["password2"]
        ):  # password와 password2가 일치하는지 확인
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )
        return attrs  # 문제가 없으면 검증된 데이터 반환

    def create(self, validated_data):  # 사용자 생성: serializer.save() 호출 시 실행됨
        user = User.objects.create_user(  # Django User 생성, create_user()는 내부적으로 비밀번호를 hash 처리함
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user
