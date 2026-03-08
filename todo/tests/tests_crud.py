from django.test import TestCase  # django.test에 TestCase 모듈 불러와줘.
from rest_framework.test import (
    APIClient,
)  # rest_framework.test에 APIClient 모듈 불러와줘.

from ..models import Todo


class TodoAPITests(TestCase):  # 클래스 기반 TodoAPITests를 만들거야
    def setUp(self):  #  각 테스트 함수가 실행되기 전마다 setUp 함수 실행시켜줘
        self.client = APIClient()  # APIClient 모듈을 self.client로 불러와줘
        self.todo = Todo.objects.create(  # Todo 테이블에서 새롭게 생성할 데이터를 self.todo 변수에 담아줘
            name="운동",
            description="스쿼트 50회",
            complete=False,
            exp=10,
        )

    def test_list(self):  # test_list 함수 실행시켜줘.
        res = self.client.get(
            "/todo/api/list/"
        )  # /todo/api/list/ 주소로 GET 요청을 보내고 그 응답을 res 변수에 담아줘
        self.assertEqual(
            res.status_code, 200
        )  # res 변수에서 담아올 때 http 상태코드가 200과 일치하는지 점검해줘
        self.assertIsInstance(
            res.json(), list
        )  # res 변수로 응답받은 JSON 데이터가 list 형식인지 점검해줘

    def test_create(self):  # test_create 함수 실행시켜줘
        payload = {  # payload 변수에 딕셔너리 데이터를 담아줘
            "name": "공부",
            "description": "DRF",
            "complete": False,
            "exp": 5,
        }
        res = self.client.post(
            "/todo/api/create/", payload, format="json"
        )  # res 변수에 "/todo/api/create/"에 post 요청해서 payload 데이터를 json 형식으로 생성해줘
        self.assertEqual(
            res.status_code, 201
        )  # res 변수에 생성된 과정 중 http 상태가 201인지 점검해줘
        self.assertEqual(
            Todo.objects.count(), 2
        )  # res 변수: setUp에서 1개 생성 + 지금 1개 생성 = Todo 테이블 전체 데이터가 2개인지 점검해줘

    def test_retrieve(self):  # test_retrieve 함수 실행시켜줘
        res = self.client.get(
            f"/todo/api/retrieve/{self.todo.id}/"
        )  # setUp에서 생성한 todo의 id로 /todo/api/retrieve/{id}/ 에 GET 요청을 보내고 응답을 res에 담아줘
        self.assertEqual(
            res.status_code, 200
        )  # res 변수에 데이터 불러오는 과정이 성공적이면 http 상태를 200인지 점검해줘
        self.assertEqual(
            res.json()["name"], "운동"
        )  # res 변수에 불러온 데이터 "name"이 "운동"인지 점검해줘

    def test_update_patch(self):  # test_update_patch 함수 실행시켜줘
        payload = {"name": "운동(수정)"}  # payload 변수에 딕셔너리 데이터 담아줘
        res = self.client.patch(
            f"/todo/api/update/{self.todo.id}/", payload, format="json"
        )  # res 변수에 payload 데이터에 담은 값을 json 형식으로 수정요청해서 결과값 담아줘
        self.assertEqual(
            res.status_code, 200
        )  # payload 데이커로 수정돼서 http 상태가 200인지 점검해줘
        self.todo.refresh_from_db()  # DB에서 최신 데이터를 다시 불러와서 self.todo를 업데이트해줘
        self.assertEqual(
            self.todo.name, "운동(수정)"
        )  # refresh_from_db()로 갱신한 self.todo의 name이 "운동(수정)"으로 바뀌었는지 점검해줘

    def test_delete(self):  # test_delete 함수 실행시켜줘
        res = self.client.delete(
            f"/todo/api/delete/{self.todo.id}/"
        )  # setUp에서 생성한 todo의 id로 /todo/api/delete/{id}/ 에 DELETE 요청을 보내고 응답을 res에 담아줘
        self.assertEqual(
            res.status_code, 204
        )  # 요청한 데이터가 삭제됐다면 http 상태가 204인지 점검해줘
        self.assertFalse(
            Todo.objects.filter(id=self.todo.id).exists()
        )  # DB에서 self.todo.id와 일치하는 데이터를 조회했을 때 존재하지 않는지 점검해줘

    def test_not_found_returns_404(self):  # test_not_found_return_404 함수 실행시켜줘
        res = self.client.get(
            "/todo/api/retrieve/999999/"
        )  # DB에 존재하지 않는 pk(999999)로 GET 요청을 보내고 응답을 res에 담아줘
        self.assertEqual(
            res.status_code, 404
        )  # 데이터가 없어서 http 상태가 404인지 점검해줘
