from rest_framework import (
    serializers,
)  # Django REST Framework에서 serializers 기능 가져올게(DB 데이터를 JSON 형식으로 변환하거나, JSON 데이터를 DB에 저장할 수 있게 해주는 기능)
from .models import (
    CollectedReview,
)  # 같은 폴더의 models.py 파일에서 CollectedReview 클래스 가져올게


class CollectedReviewSerializer(
    serializers.ModelSerializer
):  # ModelSerializer를 기반으로 CollectedReviewSerializer 클래스 생성할게(CollectedReview 모델 데이터를 JSON으로 변환해주는 Serializer야)
    class Meta:  # Serializer 동작 방식을 설정하는 Meta 클래스 선언할게 (어떤 모델을, 어떤 필드로 변환할지 지정하는 곳이야)
        model = CollectedReview  # 이 Serializer가 변환할 대상 모델은 CollectedReview로 지정할게
        fields = [
            "id",
            "title",
            "review",
            "doc_id",
            "collected_at",
        ]  # API 응답 JSON에 포함할 필드를 id, title, review, doc_id, collected_at으로 지정할게 (여기 없는 필드는 API 응답에서 제외돼)


class SentimentTextSerializer(serializers.Serializer):
    """
    POST로 텍스트를 직접 보내서 감정분석할 때 입력 검증용
    """

    text = serializers.CharField(allow_blank=False, max_length=5000)
