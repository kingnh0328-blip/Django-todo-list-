from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupAPIView, SessionLogoutAPIView
from .views_page import LoginPageView, SignupPageView

urlpatterns = [
    # API
    path("api/signup/", SignupAPIView.as_view(), name="api-signup"),
    # /api/signup/ 주소로 요청이 오면 SignupAPIView를 실행시켜서 JSON 데이터로 응답해줘
    path("api/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    # /api/login/ 주소로 요청이 오면 POST 요청 시 (username, password 전달) -> access 토큰 + refresh 토큰을 발급해줘
    path("api/token/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    # /api/token/refresh/ 으로 POST 요청 시 (refresh 토큰 전달) -> 만료된 access 토큰을 새로 재발급해줘
    path("api/logout/", SessionLogoutAPIView.as_view(), name="api-logout"),
    # /api/logout/ 주소로 요청이 오면 SessionLogoutAPIView를 실행시켜서 JSON 데이터로 응답해줘
    # Pages
    path("signup-page/", SignupPageView.as_view(), name="page-signup"),
    # signup-page/ 주소로 요청이 오면 탬플릿뷰 함수에 있는 SignupPageView 클래스 실행해서 HTML 화면으로 응답해줘
    path("login/", LoginPageView.as_view(), name="page-login"),
    # login/ 주소로 요청이 오면 탬플릿뷰 함수에 있는 LoginPageView 클래스 실행해서 HTML 화면으로 응답해줘
]
