from django.conf import (
    settings,
)  # Django 설정에서 AUTH_USER_MODEL 가져오기, 기본 User 모델 또는 커스텀 User 모델을 참조하기 위해 사용
from django.db import models  # Django ORM 모델 클래스 사용


# ============================================
# Todo 좋아요 모델
# ============================================
class TodoLike(models.Model):  # TodoLike 클래스를 models를 기반으로 생성할게
    user = models.ForeignKey(  # 사용자 정보는 models에 있는 데이터에 상속된 값으로 지정할게
        settings.AUTH_USER_MODEL,  # settings에 있는 승인된 사용자 데이터 불러와줘
        on_delete=models.CASCADE,  # 사용자가 삭제되면 상속된 데이터도 모두 삭제해줘
    )

    todo = models.ForeignKey(
        "todo.Todo", on_delete=models.CASCADE, related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "todo")


# ============================================
# Todo 북마크 모델
# ============================================
class TodoBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    todo = models.ForeignKey(
        "todo.Todo", on_delete=models.CASCADE, related_name="bookmarks"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "todo")


# ============================================
# Todo 댓글 모델
# ============================================
class TodoComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    todo = models.ForeignKey(
        "todo.Todo", on_delete=models.CASCADE, related_name="comments"
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
