from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# 프레임워크에서 뷰(View) 처리 후
# 사용자를 다른 URL로 강제 이동(리다이렉션)시킬 때
# 사용하는 redirect 함수를 가져오는 명령입니다.
# 주로 폼 제출 후 데이터 중복 방지나 페이지 이동을 위해 사용
# 주로 views.py에서 사용됩니다.
# render는 HTML 템플릿을 화면에 그리지만,
# redirect는 HTTP 응답을 통해 브라우저에게 다른 주소로 재요청을 보내는 방식입니다.

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: redirect("todo:list")),  # 첫 페이지가 무조건 보이게 하기
    path("todo/", include("todo.urls")),
    # request를 받으면, todo:list로 redirect해줘" 라는 이름 없는 함수를 그 자리에서 만든 것!
]
