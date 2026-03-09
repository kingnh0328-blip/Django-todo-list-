from rest_framework.pagination import (
    PageNumberPagination,
)  # rest_framework.pagination 모듈에서 PageNumberPagination 클래스를 가져와줘
from rest_framework.response import (
    Response,
)  # rest_framework.response 모듈에서 Response 클래스를 가져와줘
from collections import OrderedDict  # collections 모듈에서 OrderDict 클래스를 가져와줘
from django.conf import settings  # django.conf 모듈에서 settings 객체를 가져와줘


# ---------------------------------------------------------
# 사용자 정의 페이지네이션 클래스
# ---------------------------------------------------------
class CustomPageNumberPagination(
    PageNumberPagination
):  # PageNumberPagination을 상속받아서 커스텀 페이지네이션 클래스를 만들게
    default_page_size = settings.REST_FRAMEWORK.get(
        "PAGE_SIZE", 10
    )  # 기본 페이지 수는 settings에서 rest_framework 모듈에서 가져온 기본 값으로 설정하고 값이 없으면 10으로 설정해줘

    # ---------------------------------------------------------
    # 페이지네이션 적용 전 QuerySet 처리
    # ---------------------------------------------------------
    def paginate_queryset(
        self, queryset, request, view=None
    ):  # paginate_queryset 함수 실행시켜줘
        page_size = request.query_params.get(
            "page_size", self.default_page_size
        )  # URL에서 page_size 파라미터 값을 가져오고, 없으면 기본값(default_page_size)을 담아줘
        if page_size == "all":  # 만약 page_size가 all이면
            self.page_size = len(
                queryset
            )  # 전체 데이터 개수만큼 page_size를 설정해서 모든 데이터를 한 페이지에 보여줘

        else:  # 예외 함수
            try:
                self.page_size = int(
                    page_size
                )  # self.page_size에 사용자가 입력한 page_size를 정수로 변환해서 담아줘
            except ValueError:  # 값이 에러난 경우
                self.page_size = (
                    self.default_page_size
                )  # self.page_size 변수에 기본 페이지 값을 넣어줘
        return super().paginate_queryset(
            queryset, request, view
        )  # 부모 클래스(PageNumberPagination)의 paginate_queryset을 실행해서 페이지 나누기를 처리해줘

    # ---------------------------------------------------------
    # 페이지네이션 응답 구조 정의
    # ---------------------------------------------------------
    def get_paginated_response(self, data):  # get_paginated_response 함수 실행시켜줘

        return Response(  # 아래 데이터를 JSON 형식 응답으로 돌려줘
            OrderedDict(
                [  # 딕셔너리 값을 다음과 같이 저장해줘
                    ("data", data),  # data 변수를 "data"로 지정해줘
                    ("page_size", len(data)),  # 현재 페이지 데이터 수
                    (
                        "total_count",
                        self.page.paginator.count,
                    ),  # 전체 데이터(todo) 개수
                    ("page_count", self.page.paginator.num_pages),  # 전체 페이지 수
                    ("current_page", self.page.number),  # 현재 페이지 번호
                    ("next", self.get_next_link()),  # 다음 페이지 url
                    ("previous", self.get_previous_link()),  # 이전 페이지 url
                ]
            )
        )
