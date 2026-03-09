from django.urls import path, include
from .views.templates_views import (
    TodoListView,
    TodoCreateView,
    TodoDetailView,
    TodoUpdateView,
)

# from .views.api_views import TodoListAPI, TodoCreateAPI, TodoRetrieveAPI, TodoUpdateAPI, TodoDeleteAPI
from .views.api_views import TodoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("view", TodoViewSet, basename="todo")

urlpatterns = [
    # path("list/", views.todo_list, name="list"),
    # 첫 테스트용: 누군가 /list/ 주소로 접속하면, views.py에 있는 todo_list 함수를 실행해줘
    # 탬플릿 View
    path("list/", TodoListView.as_view(), name="todo_list"),
    # 실제 작동용 list: 누군가 /list/ 주소로 접속하면, templates_views.py에 있는 TodoListView 클래스를 뷰로 변환해서 실행해줘
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    # 실제 작동용 create: 누군가 /create/ 주소로 접속하면, templates_views.py에 있는 TodoCreateView 클래스를 뷰로 변환해서 실행해줘
    path("detail/<int:pk>/", TodoDetailView.as_view(), name="todo_Detail"),
    # 실제 작동용 detail: 누군가 /detail/1/ 주소로 접속하면, TodoDetailView를 실행해서 1번 Todo의 상세 화면을 보여줘
    path("update/<int:pk>/", TodoUpdateView.as_view(), name="todo_update"),
    # API DRF / JSON 응답 뷰
    # path("api/list/", TodoListAPI.as_view(), name="todo_api_list"),
    # /api/list/ 주소로 요청이 오면 (사람이든 프로그램이든) TodoListAPI를 실행해서 JSON 데이터로 응답해줘
    # path("api/create/", TodoCreateAPI.as_view(), name="todo_api_create"),
    # /api/create/ 주소로 요청이 오면 (사람이든 프로그램이든) TodoCreateAPI를 실행해서 JSON 데이터로 응답해줘
    # path("api/retrieve/<int:pk>/", TodoRetrieveAPI.as_view(), name="todo_api_retrieve"),
    # /api/retrieve/pk/ 주소로 요청이 오면 (사람이든 프로그램이든) TodoRetrieveAPI를 실행해서 pk번 Todo의 JSON 데이터로 응답해줘
    # path("api/update/<int:pk>/", TodoUpdateAPI.as_view(), name="todo_api_update"),
    # /api/update/pk/ 주소로 요청이 오면 (사람이든 프로그램이든) TodoUpdateAPI를 실행해서 pk번 Todo를 요청받은 JSON 데이터로 수정하고 성공하면 응답(200)을 돌려줘
    # path("api/delete/<int:pk>/", TodoDeleteAPI.as_view(), name="todo_api_delete"),
    # /api/delete/1/ 주소로 요청이 오면 (사람이든 프로그램이든) TodoDeleteAPI를 실행해서 pk번 Todo를 DB에서 삭제하고 성공하면 빈 응답(204)을 돌려줘
    # Viewsets CRUD를 하나로 통일
    path("viewsets/", include(router.urls)),
    # 127.0.0.1:8000/todo/viewsets/view/
]
