from rest_framework import (
    viewsets,
    status,
)  # Django rest_framework 에서 viewsets 기능 가져올게 (URL과 DB 데이터를 연결해서 API 응답을 자동으로 만들어주는 기능이야)

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
)  # Django rest_framework.permission 기능에서 로그인한 사옹자만 접근할 수 있는 기능 가져올게 (비로그인 사용자도 읽기(GET)는 가능하고, 쓰기(POST/DELETE 등)는 로그인해야 가능한 권한 설정이야)

from rest_framework.decorators import (
    action,
)  # Django rest_framework.decorators 기능에서 action? 가져올게

from rest_framework.response import (
    Response,
)  # Django rest_framework.response 기능에서 응답객체 불러오는 기능 가져올게

from .models import (
    CollectedReview,
)  # 같은 폴더의 models.py 파일에서 CollectedReview 클래스 가져올게

from .serializers import (
    CollectedReviewSerializer,
    SentimentTextSerializer,
)  # serializer 파일에서 CollectedReviewSerializer, SentimentTextSerializer 클래스 가져올게

from .services import (
    predict_sentiment,
)  # services 파일에서 presict_sentiment 클래스 가져올게

from django.shortcuts import render


class CollectedReviewViewSet(
    viewsets.ReadOnlyModelViewSet
):  # ReadOnlyModelViewSet을 기반으로 CollectedReviewViewSet 클래스 생성할게 (목록 조회(list)와 단건 조회(retrieve) API만 자동으로 제공해줘, 수정/삭제 API는 제공 안 해)

    queryset = CollectedReview.objects.all().order_by(
        "-id"
    )  # CollectedReview 테이블의 전체 데이터를 id 내림차순(최신순)으로 정렬해서 queryset 변수에 담아줘
    serializer_class = CollectedReviewSerializer  # API 응답 시 DB 데이터를 JSON으로 변환할 때 사용할 Serializer를 CollectedReviewSerializer로 지정할게
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 비로그인 사용자는 읽기(GET)만 가능하고, 쓰기(POST/DELETE 등)는 로그인해야 가능하도록 권한 설정할게

    @action(detail=True, methods=["get"], url_path="sentiment")
    def sentiment(self, request, pk=None):
        """
        GET /reviews/{id}/sentiment/
        DB에 저장된 review 텍스트로 감정분석
        """
        obj = self.get_object()
        if not obj.review:
            return Response(
                {"detail": "review text is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        pred = predict_sentiment(obj.review)

        return Response(
            {
                "id": obj.id,
                "title": obj.title,
                "sentiment": pred,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="sentiment",
        permission_classes=[AllowAny],
    )
    def sentiment_text(self, request):
        """
        POST /reviews/sentiment/
        body: {"text": "..."}
        텍스트 직접 보내 감정분석
        """
        serializer = SentimentTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data["text"]
        pred = predict_sentiment(text)

        return Response(pred, status=status.HTTP_200_OK)


def reviews_page(request):
    return render(request, "reviews/reviews_page.html")
