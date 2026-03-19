from django.contrib import admin  # django.cotrib에서 admin 기능 가져올게
from .models import CollectedReview  # models 파일에서 CollectedReview 가져올게


@admin.register(CollectedReview)  # CollectedReview 모델을 admin 사이트에 등록할게
class CollectedReviewAdmin(
    admin.ModelAdmin
):  # collectedreviewadmin 클래스를 modeladmin을 기반으로 생성할게
    list_display = (
        "id",
        "title",
        "doc_id",
        "collected_at",
    )  # list_display 칼럼에 id, title, doc_id, collected_at 필드 포함해줘
    search_fields = (
        "title",
        "review",
    )  # admin 검색창에서 title, review 필드로 검색 가능하게 해줘
