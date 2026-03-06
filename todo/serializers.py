# DRF의 ModelSerializer 도구를 가져오고, Todo 모델도 가져와
from rest_framework.serializers import ModelSerializer
from .models import Todo

# API 요청 데이터를 모델 객체로 변환하는 변환기


class TodoSerializer(ModelSerializer):
    # ModelSerializer를 기반으로 한 TodoSerializer를 만들게
    class Meta:
        model = Todo  # 이 Serializer는 Todo 모델을 위한 거야
        fields = "__all__"  # Todo 모델의 모든 필드를 JSON으로 변환해줘
        read_only_fields = [
            "created_at",
            "updated_at",
        ]  # created_at, updated_at은 읽기만 가능, API로 수정 못함(자동생성되는 시간이라 외부에서 바뀌면 안되기 때문)

        # fields = [
        # 이 필드들만 골라서 JSON으로 변환해줘
        #    "name",
        #    "description",
        #    "complete",
        #   "exp",
        #    "completed_at",
        #    "created_at",
        #    "updated_at",
        # ]

        # exclude = ["created_at", "updated_at"]
        # 모든 필드를 기본 포함시키고 -> 특정 필드만 제외하고 싶을 때
        # 전체 필드에서 이 두 개만 빼고 JSON으로 변환해줘
