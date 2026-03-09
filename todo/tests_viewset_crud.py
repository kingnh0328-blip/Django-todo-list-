from django.test import TestCase
from rest_framework.test import APIClient
from .models import Todo


# ---------------------------------------------------------
# ViewSet 기반 Todo CRUD API 테스트
# ---------------------------------------------------------
class TodoViewSetCRUDTests(TestCase):
    """
    ViewSet 라우팅 기반 API 테스트

    list:     GET    /todo/viewsets/view/
    create:   POST   /todo/viewsets/view/
    retrieve: GET    /todo/viewsets/view/<pk>/
    update:   PATCH  /todo/viewsets/view/<pk>/
    destroy:  DELETE /todo/viewsets/view/<pk>/
    """

    # ---------------------------------------------------------
    # 테스트 시작 전에 공통 데이터 준비
    # ---------------------------------------------------------
    def setUp(self):
        self.client = APIClient()
        self.base_url = "/todo/viewsets/view/"
        self.todo = Todo.objects.create(
            name="운동",
            description="스쿼트 50회",
            complete=False,
            exp=10,
        )
        # 테스트용 기본 Todo 데이터 생성

    # ---------------------------------------------------------
    # 목록 조회 테스트
    # ---------------------------------------------------------
    def test_list(self):
        res = self.client.get(self.base_url)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    # ---------------------------------------------------------
    # 생성 테스트
    # ---------------------------------------------------------
    def test_create(self):
        payload = {
            "name": "공부",
            "description": "DRF",
            "complete": False,
            "exp": 5,
        }
        res = self.client.post(self.base_url, payload, format="json")
        self.assertIn(res.status_code, (200, 201))
        self.assertEqual(Todo.objects.count(), 2)

    # ---------------------------------------------------------
    # 상세 조회 테스트
    # ---------------------------------------------------------
    def test_retrieve(self):
        res = self.client.get(f"{self.base_url}{self.todo.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], "운동")

    # ---------------------------------------------------------
    # 부분 수정 테스트 (PATCH)
    # ---------------------------------------------------------
    def test_partial_update_patch(self):
        payload = {"name": "운동(수정)"}
        res = self.client.patch(
            f"{self.base_url}{self.todo.id}/", payload, format="json"
        )
        self.assertEqual(res.status_code, 200)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.name, "운동(수정)")

    # ---------------------------------------------------------
    # 삭제 테스트
    # ---------------------------------------------------------
    def test_destroy_delete(self):
        res = self.client.delete(f"{self.base_url}{self.todo.id}/")
        self.assertIn(res.status_code, (200, 204))
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())

    # ---------------------------------------------------------
    # 존재하지 않는 데이터 요청 테스트
    # ---------------------------------------------------------
    def test_not_found_returns_404(self):
        res = self.client.get(f"{self.base_url}999999/")
        self.assertEqual(res.status_code, 404)
