# reviews/services.py
import os
from transformers import pipeline
from rest_framework import serializers
from .models import CollectedReview

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

MODEL_NAME = "blockenters/finetuned-nsmc-sentiment"
_pipe = None


def get_sentiment_pipe():
    global _pipe
    if _pipe is None:
        _pipe = pipeline(
            "sentiment-analysis",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
        )
    return _pipe


def normalize_label(label_raw: str) -> str:
    # 일반적인 NSMC 파인튜닝 관례: LABEL_1=positive, LABEL_0=negative
    if label_raw == "LABEL_1":
        return "positive"
    if label_raw == "LABEL_0":
        return "negative"
    return label_raw


def predict_sentiment(text: str) -> dict:
    pipe = get_sentiment_pipe()

    # 긴문장이여도 앞부분 512 토큰까지만 잘라서안전하게 추론
    result = pipe(text, truncation=True, max_length=512)[0]

    label_raw = result.get("label")
    score = float(result.get("score", 0.0))

    return {
        "model": MODEL_NAME,
        "label_raw": label_raw,
        "label": normalize_label(label_raw),
        "score": score,
    }


class CollectedReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectedReview
        fields = ["id", "title", "review", "doc_id", "collected_at"]


class SentimentTextSerializer(serializers.Serializer):
    """
    POST로 텍스트를 직접 보내서 감정분석할 때 입력 검증용
    """

    text = serializers.CharField(allow_blank=False, max_length=5000)
