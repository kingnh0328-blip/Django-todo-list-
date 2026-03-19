from django.db import models  # django db에서 models 를 가져올게


class CollectedReview(models.Model):  # model을 기반으로 CollectedRewiew 클래스 생성할게
    id = models.BigAutoField(primary_key=True)  # ✅ DB에 이미 있음

    title = models.CharField(
        max_length=255
    )  # title 칼럼은 문자열로 최대 255자 까지 가능한 데이터야
    review = models.TextField()  # review 칼럼은 문자열로 입력받을 수 있는 데이터야

    doc_id = models.CharField(
        max_length=255, null=True, blank=True
    )  # doc_id는 문자열로 최대 255자까지 입력받고 데이터 값이나 입력값이 없어도 상관없어.
    collected_at = models.DateTimeField(
        null=True, blank=True
    )  # collected_at은 날짜형식으로 받고, 값이나 입력값이 없어도 상관없어.

    class Meta:  # meta 클래스 생성할게
        db_table = "stg_movie_reviews"  # 테이블 명은 stg_movie_reviews로 해줘
        managed = False  # ✅ Django가 테이블 건드리지 않게해줘

    def __str__(self):  # 객체를 문자열로 표현할 때 사용할 함수 정의할게
        return self.title  # title 값을 반환해서 객체 이름으로 표시해줘
