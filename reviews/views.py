from rest_framework import (
    viewsets,
)  # Django rest_framework 에서 viewsets 기능 가져올게 (URL과 DB 데이터를 연결해서 API 응답을 자동으로 만들어주는 기능이야)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)  # Django rest_framework.permission 기능에서 로그인한 사옹자만 접근할 수 있는 기능 가져올게 (비로그인 사용자도 읽기(GET)는 가능하고, 쓰기(POST/DELETE 등)는 로그인해야 가능한 권한 설정이야)

from .models import (
    CollectedReview,
)  # 같은 폴더의 models.py 파일에서 CollectedReview 클래스 가져올게
from .serializers import (
    CollectedReviewSerializer,
)  # serializer 파일에서 CollectedReviewSerializer 클래스 가져올게


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
