from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .models import CollectedReview
from .services import predict_sentiment


@shared_task(bind=True)
def analyze_review_sentiment_by_id(self, review_id: int) -> dict:
    """
    DB에 있는 리뷰(id)를 가져와서 services의 AI 로직으로 감정분석 후 결과 반환
    """
    try:
        obj = CollectedReview.objects.get(id=review_id)
    except ObjectDoesNotExist:
        return {"status": "error", "detail": "review not found", "review_id": review_id}

    text = (obj.review or "").strip()
    if not text:
        return {
            "status": "error",
            "detail": "review text is empty",
            "review_id": review_id,
        }

    pred = predict_sentiment(text)

    return {
        "status": "ok",
        "review_id": obj.id,
        "title": obj.title,
        "sentiment": pred,
    }


@shared_task(bind=True)
def analyze_sentiment_text(self, text: str) -> dict:
    """
    텍스트를 직접 받아 감정분석
    """
    text = (text or "").strip()
    if not text:
        return {"status": "error", "detail": "text is empty"}

    pred = predict_sentiment(text)
    return {"status": "ok", "sentiment": pred}
