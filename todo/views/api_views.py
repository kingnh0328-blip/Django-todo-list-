from rest_framework.views import APIView  # DRF에서 API용 뷰의 기본 틀을 가져와
from rest_framework.response import Response  # API 응답을 만들어주는 도구를 가져와
from rest_framework import viewsets  # ViewSets 사용을 위한 DRF 모듈 import
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
)  # 인증된 사용자만 접근 가능하도록 하는 권한 클래스
from ..models import Todo  # 경로변경
from ..serializers import TodoSerializer  # 경로변경
from django.db.models import Q


# 전체보기
class TodoListAPI(APIView):  # APIView를 기반으로 TodoListAPI 클래스를 만들게
    def get(self, request):
        # GET 요청이 들어오면 실행되는 함수: GET 방식으로 요청이 오면 이 함수를 실행해줘(POST는 안 됨)

        todos = Todo.objects.all()
        # Todo 모델의 모든 데이터 조회 (QuerySet): DB에서 Todo 데이터를 전부 꺼내와서 todos에 담아줘

        serializer = TodoSerializer(todos, many=True)
        # 조회한 Todo 객체들을 Serializer로 JSON 변환 준비: TodoSerializer야, todos 전체를 JSON으로 변환할 준비를 해줘.
        # many=True → 여러 개의 객체를 변환한다는 의미:데이터가 여러 개야. 하나가 아니야.

        return Response(serializer.data)
        # serializer.data를 JSON 형태로 변환하여 API 응답으로 반환: 변환된 JSON 데이터를 응답으로 돌려줘


# ---------------------------------------------------------
# Todo 목록 페이지네이션 설정
# ---------------------------------------------------------
class TodoListPagination(
    PageNumberPagination
):  # PageNumberPagination을 상속받아서 TodoListPagination 커스텀 클래스 만들게
    page_size = 3  # 한 페이지에 보이는 데이터는 3개로 입력할게
    page_size_query_param = "page_size"  # url에서 시용자가 page_size 파라미터로 페이지 크기를 조절할 수 있게 허용해줘
    max_page_size = 50  # 한 페이지에 최대로 보여줄 수 있는 데이터 개수는 50개로 설정


# ---------------------------------------
# Todo ViewSet: Todo CRUD를 하나의 클래스에서 처리하는 ViewSet
# ---------------------------------------
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer  # Todo 데이터를 변환할 Serializer 지정할게
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 API 접근 가능하게 해줘
    pagination_class = TodoListPagination  # 페이지네이션 설정 적용 해줘

    def get_queryset(self):  # 사용자에게 보여줄 Todo 목록을 DB에서 가져올게
        user = self.request.user  # 사용자가 작성한 글을 검증해줘
        return Todo.objects.filter(  # todo 목록을 필터링해서 보여줄게
            Q(is_public=True) | Q(user=user)
        ).order_by(
            "-created_at"
        )  # 공개상태이거나 사용자가 작성한 글을 생성한 순서대로 출력해줘

    def perform_create(
        self, serializer
    ):  # POST 요청으로 todo를 생성할 때 자동으로 실행해줘
        serializer.save(
            user=self.request.user
        )  # 요청한 사용자 정보를 자동으로 포함해서 todo를 DB에 저장할게


# ===============================

# 생성하기
# class TodoCreateAPI(APIView):  # APIView 기반으로 TodoCreateAPI 클래스를 만들게
#     def post(self, request):
#         # POST 방식으로 요청이 들어오면 이 함수를 실행시켜줘
#         serializer = TodoSerializer(data=request.data)
#         # TodoSerializer야, 사용자가 post요청한 데이터를 JSON으로 변환할 준비를 해줘.
#         serializer.is_valid(raise_exception=True)
#         # 사용자가 입력한 serializer 변수를 검증해줘. 검증 실패하면 400 오류를 응답해줘.
#         todo = serializer.save()
#         # 검증한 serializer 변수를 todo에 담아서 저장해줘.
#         return Response(
#             TodoSerializer(
#                 todo
#             ).data,  # TodoSerializer가 JSON으로 변환한 데이터로 응답해줘.
#             status=status.HTTP_201_CREATED,  # 데이터가 문제 없이 저장되었다면 http를 201 상태로 바꿔줘.
#         )


# 상세보기 API
# class TodoRetrieveAPI(APIView):  # API 기반으로 TodoRetrieveAPI 클래스 만들게.
#     def get(self, request, pk):  # 사용자가 get 형식으로 요청하면 이 함수를 실행시켜줘.
#         try:
#             todo = Todo.objects.get(
#                 pk=pk
#             )  # url에서 받은 pk번호와 일치하는 Todo 한 개를 DB에서 찾아서 todo 변수에 담아줘
#         except (
#             Todo.DoesNotExist
#         ):  # 사용자가 get 형식으로 요청한 값이 todo 테이블에 없는 경우 이 함수를 실행시켜줘.
#             return Response(
#                 {
#                     "error": "해당하는 todo가 없습니다."
#                 },  # "해당하는 todo가 없다"고 오류 메세지 입력해줘.
#                 status=status.HTTP_404_NOT_FOUND,  # http 상태는 404 오류로 출력해줘.
#             )
#         serializer = TodoSerializer(
#             todo
#         )  # Todoserializer야, DB에서 찾아온 todo 객체를 JSON으로 변환할 준비해줘
#         return Response(
#             serializer.data
#         )  # 사용자가 get 형식으로 요청한 데이터를 json으로 변환해서 응답해줘


# 수정하기 API
# class TodoUpdateAPI(APIView):  # API 기반으로 TodoUpdateAPI 클래스 만들게.
#     def put(self, request, pk):  # 사용자가 put 형식으로 요청하면 이 함수 실행시켜줘.
#         try:
#             todo = Todo.objects.get(
#                 pk=pk
#             )  # url에서 받은 pk번호와 일치하는 Todo 한 개를 DB에서 찾아서 todo 변수에 담아줘.
#         except (
#             Todo.DoesNotExist
#         ):  # pk 번호와 일치하는 todo 가 없다면 이 블록을 실행해줘
#             return Response(
#                 {
#                     "error": "해당하는 todo가 없습니다."
#                 },  # "해당하는 todo가 없다"고 오류메세지 입력해줘.
#                 status=status.HTTP_404_NOT_FOUND,  # http 상태는 404 오류로 출력해줘.
#             )

#         serializer = TodoSerializer(
#             todo, data=request.data
#         )  # TodoSerializer야, 기존 todo에 사용자가 입력한 새 데이터를 덮어씌울 준비해줘.
#         serializer.is_valid(
#             raise_exception=True
#         )  # 사용자가 입력한 data를 json으로 변환하기 전 형식이 유효한지 검증해줘
#         todo = serializer.save()  # 검증된 serializer를 todo 변수에 담아줘
#         return Response(
#             serializer.data
#         )  # serializer에서 json으로 변환한 형식으로 응답해줘.

#     def patch(self, request, pk):
#         # PATCH 요청 → 부분 수정 (일부 필드만 수정 가능)
#         try:
#             todo = Todo.objects.get(pk=pk)
#             # pk에 해당하는 Todo 데이터 조회

#         except Todo.DoesNotExist:
#             # 해당 Todo가 존재하지 않을 경우
#             return Response(
#                 {"error": "해당하는 todo가 없습니다."},
#                 status=status.HTTP_404_NOT_FOUND,
#                 # HTTP 상태코드 404 반환
#             )

#         serializer = TodoSerializer(todo, data=request.data, partial=True)
#         # partial=True → 일부 필드만 보내도 수정 가능
#         serializer.is_valid(raise_exception=True)
#         # 데이터 유효성 검사
#         todo = serializer.save()
#         # 수정된 데이터 DB 저장
#         serializer = TodoSerializer(todo)
#         # 수정된 객체를 JSON 변환

#         return Response(serializer.data)
#         # 수정된 데이터 응답


# # 삭제하기 API
# class TodoDeleteAPI(APIView):  # api 기반으로 TodoDeleteAPI 클래스 만들게.
#     def delete(self, request, pk):  # 사용자가 put 형식으로 요청하면 이 함수 실행시켜줘
#         try:
#             todo = Todo.objects.get(
#                 pk=pk  # Todo 테이블에서 사용자가 입력한 pk와 일치하는 todo를 todo 변수에 담아줘
#             )
#         except (
#             Todo.DoesNotExist
#         ):  # todo 테이블에 없는 데이터를 불러오기 할 경우 이 함수를 실행시켜줘.
#             return Response(
#                 {"error": "해당하는 todo가 없습니다."},  # 에러 메세지 띄워주고,
#                 status=status.HTTP_404_NOT_FOUND,  # http 상태는 404 상태로 출력해줘
#             )

#         todo.delete()  # DB에서 해당 todo 객체를 삭제해줘

#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )  # 삭제에 성공하면 http 상태를 204로 출력해줘
