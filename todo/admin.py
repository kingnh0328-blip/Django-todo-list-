from django.contrib import admin
from .models import Todo

# 간단 등록: Todo 모델을 관리자 페이지에 등록
# admin.site.register(Todo)Todo 모델을 관리자 페이지에 등록


# 클래스 방식 등록: Todo 모델을 관리자 페이지에 등록하는데, 이 설정대로 꾸며줘
@admin.register(Todo)  # 아래 클래스를 Todo 모델의 관리 설정으로 연결
class TodoAdmin(admin.ModelAdmin):  # 관리자 페이지 설정을 담는 그릇
    list_display = (  # 목록 화면에 어떤 컬럼을 보여줄지 지정
        "__str__",  # 모델의 `__str__` 메서드 결과값 (보통 제목)
        "created_at",  # 생성일 컬럼 표시
        "updated_at",  # 수정일 컬럼 표시
    )
