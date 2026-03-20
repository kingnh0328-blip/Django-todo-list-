from rest_framework.routers import (
    DefaultRouter,
)  # Django REST Framework의 routers에서 DefaultRouter 기능 가져올게 (ViewSet을 등록하면 URL 패턴을 자동으로 만들어주는 기능이야)
from .views import (
    CollectedReviewViewSet,
)  # 같은 폴더의 views.py 파일에서 CollectedReviewViewSet 클래스 가져올게

router = (
    DefaultRouter()
)  # DefaultRouter 클래스로 router 객체를 생성해서 router 변수에 담아줘 (이제 이 router에 ViewSet을 등록하면 URL이 자동으로 만들어져)

router.register(
    r"collected-reviews", CollectedReviewViewSet, basename="collected-reviews"
)
# router에 ViewSet을 등록할게
# (r"collected-reviews": API URL 경로 / CollectedReviewViewSet: 연결할 ViewSet 클래스
#  basename="collected-reviews": URL 이름 패턴의 기준이 되는 별칭)
# → /api/collected-reviews/ 와 /api/collected-reviews/{id}/ URL이 자동으로 생성돼

urlpatterns = router.urls
