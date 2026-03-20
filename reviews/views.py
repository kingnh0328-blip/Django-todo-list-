from rest_framework import (
    viewsets,
    status,
)  # Django rest_framework 에서 viewsets 기능 가져올게 (URL과 DB 데이터를 연결해서 API 응답을 자동으로 만들어주는 기능이야)


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


from celery.result import AsyncResult

from .tasks import analyze_review_sentiment_by_id, analyze_sentiment_text
from django.shortcuts import render


def reviews_page(request):
    return render(request, "reviews/reviews_page.html", {})


class CollectedReviewViewSet(
    viewsets.ReadOnlyModelViewSet
):  # ReadOnlyModelViewSet을 기반으로 CollectedReviewViewSet 클래스 생성할게 (목록 조회(list)와 단건 조회(retrieve) API만 자동으로 제공해줘, 수정/삭제 API는 제공 안 해)

    queryset = CollectedReview.objects.all().order_by(
        "-id"
    )  # CollectedReview 테이블의 전체 데이터를 id 내림차순(최신순)으로 정렬해서 queryset 변수에 담아줘
    serializer_class = CollectedReviewSerializer  # API 응답 시 DB 데이터를 JSON으로 변환할 때 사용할 Serializer를 CollectedReviewSerializer로 지정할게

    # ---------------------------------------------------------
    # ✅ (A) DB 리뷰 비동기 분석 시작: job_id 즉시 반환
    # POST /api/reviews/collected-reviews/{id}/sentiment-async/
    # ---------------------------------------------------------
    @action(detail=True, methods=["post"], url_path="sentiment-async")
    def sentiment_async(self, request, pk=None):
        review_id = int(pk)
        task = analyze_review_sentiment_by_id.delay(review_id)

        return Response(
            {"task_id": task.id, "status": "queued"}, status=status.HTTP_202_ACCEPTED
        )

    # ---------------------------------------------------------
    # ✅ (B) 텍스트 비동기 분석 시작
    # POST /api/reviews/collected-reviews/sentiment-async/
    # body: {"text": "..."}
    # ---------------------------------------------------------
    @action(detail=False, methods=["post"], url_path="sentiment-async")
    def sentiment_text_async(self, request):
        serializer = SentimentTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data["text"]
        task = analyze_sentiment_text.delay(text)

        return Response(
            {"task_id": task.id, "status": "queued"}, status=status.HTTP_202_ACCEPTED
        )

    # ---------------------------------------------------------
    # ✅ (C) 결과 조회
    # GET /api/reviews/collected-reviews/sentiment-result/{task_id}/
    # ---------------------------------------------------------
    @action(
        detail=False, methods=["get"], url_path=r"sentiment-result/(?P<task_id>[^/.]+)"
    )
    def sentiment_result(self, request, task_id=None):
        res = AsyncResult(task_id)

        payload = {"task_id": task_id, "state": res.state}

        if res.state == "PENDING":
            return Response(payload, status=status.HTTP_200_OK)

        if res.state == "FAILURE":
            payload["error"] = str(res.result)
            return Response(payload, status=status.HTTP_200_OK)

        # SUCCESS
        if res.state == "SUCCESS":
            payload["result"] = res.result
            return Response(payload, status=status.HTTP_200_OK)

        # STARTED / RETRY 등
        return Response(payload, status=status.HTTP_200_OK)
