from django.shortcuts import render
from ..models import Todo
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy


# 함수형
def todo_list(request):
    todos = Todo.objects.all()
    return render(request, "todo/todo.html", {"todos": todos})


# ----------------

# 클래스형

# GET 방식으로 /list/ 에 접속하면,
# DB에서 Todo 전체를 가져와서,
# todo.html 템플릿에
# todos 라는 이름으로 넘겨서 보여줘


# class TodoListView(View):  # 클래스형
#     def get(self, request):
#         todos = Todo.objects.all()
#         return render(request, "todo/todo.html", {"todos": todos})


# ----------------

# 제너릭뷰

# > Todo 모델의 전체 목록을 보여주는 뷰야.
# > 화면은 todo.html을 써줘.
# > 템플릿에서 데이터는 `todos` 라는 이름으로 불러줘.


class TodoListGenericView(ListView):
    model = Todo
    template_name = "todo/todo.html"  # 기본값: todo_list.html
    context_object_name = "todos"  # 기본값: object_list


# ===============
# 목록 조회
class TodoListView(ListView):
    model = Todo
    # 이 뷰가 사용할 모델 지정 (Todo 테이블 데이터를 조회)
    template_name = "todo/list.html"
    # 데이터를 보여줄 HTML 템플릿 파일 지정
    context_object_name = "todos"
    # 템플릿에서 사용할 변수 이름 (기본값 object_list 대신 todos 사용)
    ordering = ["-created_at"]
    # 데이터 정렬 방식 (created_at 기준 내림차순 → 최신 글이 먼저)
    success_url = reverse_lazy("todo:list")
    # 작업 성공 후 이동할 URL (ListView에서는 보통 사용하지 않지만 설정 가능)


# ===============
# todo 생성하기
class TodoCreateView(CreateView):
    model = Todo
    # 이 뷰에서 사용할 모델 (Todo 테이블에 데이터 생성)
    fields = ["name", "description", "complete", "exp"]
    # HTML form에서 입력받을 모델 필드 정의
    template_name = "todo/create.html"
    # Todo 생성 화면에 사용할 템플릿 파일
    success_url = reverse_lazy("todo:list")
    # 생성이 성공하면 이동할 url (todo 목록 페이지)


# ===============
# todo 상세보기
class TodoDetailView(DetailView):
    model = Todo
    # 이 뷰에서 사용할 모델 (Todo 테이블 데이터를 조회)
    template_name = "todo/detail.html"
    # Todo 상세보기 화면에 사용할 템플릿 파일
    context_object_name = "todo"
    # 템플릿에서 사용할 변수 이름(기본값 object 대신 todo 사용, todos가 아닌 이유: 한개만 상세보기로 볼 수 있기 때문에)


# ===============
# todo 수정하기
class TodoUpdateView(UpdateView):
    model = Todo  # 이 뷰가 사용할 모델 지정(Todo 테이블의 데이터를 조회)
    fields = ["name", "description", "complete", "exp"]  # 뷰에서 사용할 필드 값 지정
    template_name = "todo/update.html"  # 뷰 로직을 출력할 템플릿 지정
    context_object_name = "todo"  # 데이터의 기본값 대신 "todo" 사용
    success_url = reverse_lazy(
        "todo:list"
    )  # 수정 성공 시 돌아갈 화면 설정(todo 목록 페이지)
