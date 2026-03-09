from django.db import models
from django.utils import timezone


class Todo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    # True 혹은 False만 저장하는 필드
    exp = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    # 해당 날짜/시간 필드를 데이터베이스와 폼 입력 모두에서 비워둘 수 있게(Optional) 허용하는 설정
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일자
    updated_at = models.DateTimeField(auto_now=True)  # 수정일자
    image = models.ImageField(upload_to="todo_images/", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # save 함수 실행
        if (
            self.complete and self.completed_at is None
        ):  # 만약 사용자가 입력한 값이 완료 상태인데 완료 시간이 아직 기록되지 않았다면
            self.completed_at = timezone.now()  # 현재 시간값을 데이터에 입력해줘

        if (
            not self.complete and self.completed_at is not None
        ):  # 만약 사용자가 입력한 값이 완료 취소 상태인데 완료 시간이 남아있다면
            self.completed_at = None

        super().save(
            *args, **kwargs
        )  # 부모 클래스(models.Model)의 save 함수에 인자들을 그대로 전달해서 실제 DB 저장해줘
