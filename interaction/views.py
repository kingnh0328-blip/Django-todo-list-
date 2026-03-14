from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from todo.models import Todo
from .models import TodoLike, TodoBookmark, TodoComment
from .serializers import TodoCommentSerializer


# =========================================================
# 좋아요 토글 API
# POST /interaction/like/<todo_id>/
# =========================================================
class TodoLikeToggleAPIView(
    APIView
):  # APIView를 기반으로 TodoLikeToggleAPIView 클래스 생성할게
    permission_classes = [IsAuthenticated]  # 로그인 된 사용자만 접속 가능해

    def post(self, request, todo_id):  # post 요청이 들어오면 이 함수 실행해줘
        todo = get_object_or_404(
            Todo, id=todo_id
        )  # todo 변수에 Todo 테이블에서 가져온 todo_id와 일치하는 값을 담아주고 없으면 404 상태로 저장해줘

        obj, created = TodoLike.objects.get_or_create(
            todo=todo, user=request.user
        )  # TodoLike 테이블에서 해당 todo와 user 조합을 조회하고, 없으면 새로 생성해줘. obj에는 객체를, created에는 새로 생성 여부(True/False)를 담아줘.
        if not created:  # 이미 좋아요가 존재했던 경우
            obj.delete()  # 좋아요 취소 (삭제)
            liked = False  # liked 상태 False로 변경
        else:
            liked = True  # 좋아요 새로 생성됨

        count = TodoLike.objects.filter(
            todo=todo
        ).count()  # count 변수에 TodoLike 테이블에서 todo 변수에 저장된 좋아요 개수를 담아줘

        return Response(
            {
                "liked": liked,
                "like_count": count,
            }  # 현재 좋아요 상태, 총 좋아요 수를 응답객체에 담아줘
        )


# =========================================================
# 북마크 토글 API
# POST /interaction/bookmark/<todo_id>/
# =========================================================
class TodoBookmarkToggleAPIView(
    APIView
):  # APIView를 기반으로 TodoBookmarkToggleAPIView 클래스 생성할게
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근할 수 있어

    def post(self, request, todo_id):  # post 요청이 들어오면 이 함수 실행시켜줘

        todo = get_object_or_404(
            Todo, id=todo_id
        )  # Todo 테이블에서 id가 일치하는 todo가 있으면 todo 변수에 담아주고 없으면 404 상태를 담아줘.

        obj, created = TodoBookmark.objects.get_or_create(
            todo=todo, user=request.user
        )  # TodoBookmark 테이블에서 todo와 user 조합을 조회하고 없으면 새로 생성해줘, obj에는 북마크 객체를, created에는 새로 생성 여부(True/False)를 담아줘.

        if not created:  # 사용자가 새롭게 생성하지 않았다면

            obj.delete()  # obj 변수 데이터를 삭제해줘
            bookmarked = False  # bookmarked 상태도 false로 바꿔줘

        else:
            bookmarked = True  # bookmarked 상태를 true로 바꿔줘

        count = TodoBookmark.objects.filter(
            todo=todo
        ).count()  # TodoBookmark 테이블에서 todo에 해당하는 데이터의 북마크 개수를 count 변수에 담아줘

        return Response(  #  사용자에게 응답객체 반환해줘
            {
                "bookmarked": bookmarked,  # 현재 북마크 상태
                "bookmark_count": count,  # 전체 북마크 수
            }
        )


# =========================================================
# 댓글 등록 API
# POST /interaction/comment/<todo_id>/
# =========================================================
class TodoCommentCreateAPIView(
    APIView
):  # APIView 기반으로 TodoCommentCreateAPIView 클래스를 생성할게
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근할 수 있어

    def post(self, request, todo_id):  # post 요청 들어오면 다음 함수 실행시켜줘

        todo = get_object_or_404(
            Todo, id=todo_id
        )  # todo 변수에 Todo 테이블을 조회해서 id와 일치하는 todo를 담아주고 없으면 404 상태를 담아줘

        content = request.data.get(
            "content", ""
        ).strip()  # 사용자가 요청으로 보낸 데이터에서 "content" 값을 꺼내고 앞뒤 공백을 제거해서 content 변수에 담아줘

        if not content:  # content 변수에 내용이 없다면

            return Response(
                {"detail": "내용이 필요합니다."}, status=400
            )  # 400 상태와 오류 메세지로 응답해줘

        comment = TodoComment.objects.create(  # comment 변수에 TodoComment 테이블에 create 요청으로 사용자가 입력한 값을 담아줘
            todo=todo,  # 어떤 Todo에 달렸는지
            user=request.user,  # 작성자
            content=content,  # 댓글 내용
        )

        serializer = TodoCommentSerializer(
            comment
        )  # comment 객체를 TodoCommentSerializer로 딕셔너리 형태로 직렬화할 준비해줘

        return Response(
            serializer.data
        )  # 직렬화된 serializer 데이터를 응답객체에 담아줘


# =========================================================
# 댓글 목록 조회 API
# GET /interaction/comment/<todo_id>/
# =========================================================
class TodoCommentListAPIView(
    APIView
):  # APIView를 기반으로 TodoCommentListAPIView 클래스 만들거야
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def get(self, request, todo_id):  # get 요청이 들어오면 이 함수를 실행해줘

        todo = get_object_or_404(
            Todo, id=todo_id
        )  # Todo 테이블에서 todo_id와 일치라는 todo를 가져오거나 값이 없으면 404 상태로 저장해줘

        comments = TodoComment.objects.filter(todo=todo).order_by(
            "-created_at"
        )  # 특정 Todo에 달린 댓글을 최신순으로 정렬해서 comment 변수에 담아줘

        serializer = TodoCommentSerializer(  # TodoCommentSerializer로 파이썬 객체를 딕셔너리 형태로 직렬화할 준비해줘
            comments, many=True  # 여러 개 객체이기 때문에 many=True
        )

        return Response(
            serializer.data
        )  # serializer로 검증한 데이터를 응답객체로 반환해줘
