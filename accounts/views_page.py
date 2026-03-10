from django.views.generic import (
    TemplateView,
)  # Django 내장 라이브러리에서 HTML 템플릿을 렌더링해주는 TemplateView 클래스를 가져올게


class SignupPageView(
    TemplateView
):  # TemplateView 클래스 기반으로 SignupPageView 클래스 만들거야
    template_name = "accounts/signup.html"  # accout/signup.html 템플릿 파일과 연동해줘


class LoginPageView(
    TemplateView
):  # TemplateView클래스 기반으로 LoginPageView 클래스 만들거야
    template_name = "accounts/login.html"  # accounts/login.html 템플릿 파일과 연동해줘
