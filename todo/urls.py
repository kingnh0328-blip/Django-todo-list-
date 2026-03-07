from django.urls import path
from .views.templates_views import (
    TodoListView,
    TodoCreateView,
    TodoDetailView,
    TodoUpdateView,
)
from .views.api_views import (
    TodoListAPI,
    TodoCreateAPI,
    TodoRetrieveAPI,
    TodoUpdateAPI,
    TodoDeleteAPI,
)

app_name = "todo"

urlpatterns = [
    # path("list/", views.todo_list, name="list"),
    # 첫 테스트용: 누군가 /list/ 주소로 접속하면, views.py에 있는 todo_list 함수를 실행해줘
    # 탬플릿 View
    path("list/", TodoListView.as_view(), name="list"),
    # 실제 작동용 list: 누군가 /list/ 주소로 접속하면, templates_views.py에 있는 TodoListView 클래스를 뷰로 변환해서 실행해줘
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    # 실제 작동용 create: 누군가 /create/ 주소로 접속하면, templates_views.py에 있는 TodoCreateView 클래스를 뷰로 변환해서 실행해줘
    path("detail/<int:pk>/", TodoDetailView.as_view(), name="todo_Detail"),
    # 실제 작동용 detail: 누군가 /detail/1/ 주소로 접속하면, TodoDetailView를 실행해서 1번 Todo의 상세 화면을 보여줘
    path("update/<int:pk>/", TodoUpdateView.as_view(), name="todo_update"),
    # API View
    path("api/list/", TodoListAPI.as_view(), name="todo_api_list"),
    path("api/create/", TodoCreateAPI.as_view(), name="todo_api_create"),
    path("api/retrieve/<int:pk>/", TodoRetrieveAPI.as_view(), name="todo_api_retrieve"),
    path("api/update/<int:pk>/", TodoUpdateAPI.as_view(), name="todo_api_update"),
    path("api/delete/<int:pk>/", TodoDeleteAPI.as_view(), name="todo_api_delete"),
    # /api/list/ 주소로 요청이 오면 (사람이든 프로그램이든) TodoListAPI를 실행해서 JSON 데이터로 응답해줘
    # /api/create/ 주소로 요청이 오면 (사람이든 프로그램이든) TodoCreateAPI를 실행해서 JSON 데이터로 응답해줘
    # /api/retrieve/pk/ 주소로 요청이 오면 (사람이든 프로그램이든) TodoRetrieveAPI를 실행해서 pk번 Todo의 JSON 데이터로 응답해줘
]  # /api/delete/1/ 주소로 요청이 오면 (사람이든 프로그램이든) TodoDeleteAPI를 실행해서 pk번 Todo를 DB에서 삭제하고 성공하면 빈 응답(204)을 돌려줘
