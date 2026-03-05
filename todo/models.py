from django.db import models


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

    def __str__(self):
        return self.name
