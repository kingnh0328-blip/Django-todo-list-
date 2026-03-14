# DRF의 ModelSerializer 도구를 가져오고, Todo 모델도 가져와
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Todo
from interaction.models import TodoLike, TodoBookmark, TodoComment

# API 요청 데이터를 모델 객체로 변환하는 변환기


# ---------------------------------------------------------
# TodoSerializer
# ---------------------------------------------------------
# Todo 모델을 JSON 형태로 변환하는 Serializer
#
# 역할
#
# 1️⃣ Todo 모델 데이터를 JSON으로 변환
# 2️⃣ 추가 정보 계산 (좋아요 수 / 북마크 수 / 댓글 수)
# 3️⃣ 현재 로그인 사용자가 좋아요/북마크 했는지 판단
# ---------------------------------------------------------
class TodoSerializer(ModelSerializer):

    # -----------------------------------------------------
    # username 필드
    # -----------------------------------------------------
    # Todo 모델에는 user FK가 있습니다.
    #
    # user.username 값을 가져와서
    # username이라는 필드로 JSON에 포함합니다.
    #
    # source="user.username"
    # → user 모델의 username 필드를 가져옴
    #
    # read_only=True
    # → 읽기 전용 (입력 불가)
    username = serializers.CharField(source="user.username", read_only=True)

    # -----------------------------------------------------
    # 좋아요 관련 필드
    # -----------------------------------------------------

    # 좋아요 개수
    like_count = serializers.SerializerMethodField()

    # 현재 사용자가 좋아요 했는지 여부
    is_liked = serializers.SerializerMethodField()

    # -----------------------------------------------------
    # 북마크 관련 필드
    # -----------------------------------------------------

    # 북마크 개수
    bookmark_count = serializers.SerializerMethodField()

    # 현재 사용자가 북마크 했는지 여부
    is_bookmarked = serializers.SerializerMethodField()

    # -----------------------------------------------------
    # 댓글 개수
    # -----------------------------------------------------
    comment_count = serializers.SerializerMethodField()

    # -----------------------------------------------------
    # Serializer Meta 설정
    # -----------------------------------------------------
    class Meta:

        # 어떤 모델을 직렬화할지 지정
        model = Todo

        # JSON으로 변환할 필드 목록
        fields = [
            # 기본 Todo 필드
            "id",
            "name",
            "description",
            "complete",
            "exp",
            "image",
            "created_at",
            # 사용자 정보
            "user",
            "username",
            # 공개 여부
            "is_public",
            "username",
            # 좋아요 관련
            "like_count",
            "is_liked",
            # 북마크 관련
            "bookmark_count",
            "is_bookmarked",
            # 댓글 수
            "comment_count",
        ]

        # 읽기 전용 필드
        # → 클라이언트에서 수정 불가
        read_only_fields = ["user"]

    # -----------------------------------------------------
    # 현재 로그인 사용자 가져오는 함수
    # -----------------------------------------------------
    # serializer는 request 객체를 직접 접근할 수 없기 때문에
    # context를 통해 request를 전달받습니다.
    #
    # view에서
    #
    # serializer = TodoSerializer(..., context={"request": request})
    #
    # 이렇게 전달됩니다.
    #
    # 이 함수는
    # 로그인된 사용자를 반환합니다.
    def _user(self):

        # serializer context에서 request 가져오기
        request = self.context.get("request")

        # 로그인 상태 확인
        if request and request.user.is_authenticated:
            return request.user

        # 로그인 안 된 경우
        return None

    # -----------------------------------------------------
    # 좋아요 개수 계산
    # -----------------------------------------------------
    # SerializerMethodField는
    #
    # get_필드명
    #
    # 형식의 함수가 필요합니다.
    #
    # 즉
    # like_count → get_like_count
    def get_like_count(self, obj):

        # TodoLike 테이블에서
        # 해당 todo의 좋아요 개수 계산
        return TodoLike.objects.filter(todo=obj).count()

    # -----------------------------------------------------
    # 현재 사용자가 좋아요 눌렀는지 여부
    # -----------------------------------------------------
    def get_is_liked(self, obj):

        # 현재 로그인 사용자
        user = self._user()

        # 로그인 안한 경우
        if not user:
            return False

        # 좋아요 존재 여부 확인
        return TodoLike.objects.filter(todo=obj, user=user).exists()

    # -----------------------------------------------------
    # 북마크 개수 계산
    # -----------------------------------------------------
    def get_bookmark_count(self, obj):

        return TodoBookmark.objects.filter(todo=obj).count()

    # -----------------------------------------------------
    # 현재 사용자가 북마크 했는지 여부
    # -----------------------------------------------------
    def get_is_bookmarked(self, obj):

        # 현재 사용자
        user = self._user()

        if not user:
            return False

        return TodoBookmark.objects.filter(todo=obj, user=user).exists()

    # -----------------------------------------------------
    # 댓글 개수 계산
    # -----------------------------------------------------
    def get_comment_count(self, obj):

        return TodoComment.objects.filter(todo=obj).count()


# class TodoSerializer(ModelSerializer):
#     # ModelSerializer를 기반으로 한 TodoSerializer를 만들게
#     class Meta:
#         model = Todo  # 이 Serializer는 Todo 모델을 위한 거야
#         fields = "__all__"  # Todo 모델의 모든 필드를 JSON으로 변환해줘
#         read_only_fields = [
#             "created_at",
#             "updated_at",
#             "users",
#         ]  # created_at, updated_at은 읽기만 가능, API로 수정 못함(자동생성되는 시간이라 외부에서 바뀌면 안되기 때문)

# fields = [
# 이 필드들만 골라서 JSON으로 변환해줘
#    "name",
#    "description",
#    "complete",
#    "exp",
#    "completed_at",
#    "created_at",
#    "updated_at",
# ]

# exclude = ["created_at", "updated_at"]
# 모든 필드를 기본 포함시키고 -> 특정 필드만 제외하고 싶을 때
# 전체 필드에서 이 두 개만 빼고 JSON으로 변환해줘
