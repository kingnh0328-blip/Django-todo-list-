from rest_framework import serializers
from .models import TodoLike, TodoBookmark, TodoComment


# ============================================
# Todo 좋아요 Serializer
# ============================================
class TodoLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoLike
        fields = "__all__"


# ============================================
# Todo 북마크 Serializer
# ============================================
class TodoBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoBookmark
        fields = "__all__"


# ============================================
# Todo 댓글 Serializer
# ============================================
class TodoCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = TodoComment
        fields = [
            "id",  # 댓글 id
            "todo",  # 어떤 Todo에 달린 댓글인지
            "user",  # 댓글 작성자
            "username",  # 작성자 username (추가 필드)
            "content",  # 댓글 내용
            "created_at",  # 작성 시간
        ]
        read_only_fields = ["user"]
