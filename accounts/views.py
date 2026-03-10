from django.contrib.auth import authenticate, login, logout

# authenticate: 아이디/비밀번호 확인 후 User 객체 반환 (실패 시 None)
# login: 인증된 User를 세션에 저장해 로그인 상태 유지
# logout: 세션에서 사용자 정보 삭제해 로그아웃 처리
from rest_framework.views import (
    APIView,
)  # 클래스 기반 뷰(CBV)의 기본 클래스, HTTP 메서드별로 로직 작성 가능
from rest_framework.response import (
    Response,
)  # 딕셔너리 데이터를 JSON으로 변환해서 반환하는 응답 객체
from rest_framework import (
    status,
)  # HTTP 상태코드를 숫자 대신 이름으로 사용 (예: status.HTTP_200_OK)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)  # AllowAny(비로그인 사용자도 접근 허용), IsAuthenticated(로그인한 사용자만 접근 가능)
from .serializers import (
    SignupSerializer,
)  # 같은 앱의 serializers.py에서 SignupSerializer 클래스 가져오기


# -----------------------------
# 회원가입 API
# -----------------------------
class SignupAPIView(APIView):  # APIView를 기반으로 SignupAPIView 클래스 생성할게
    permission_classes = [
        AllowAny
    ]  # 이 클래스에는 로그인하지 않은 사용자도 접근할 수 있어

    def post(self, request):  # 이 함수는 post요청이 들어오면 실행시켜줘
        serializer = SignupSerializer(
            data=request.data
        )  # 요청으로 받은 데이터를 SignupSerializer에 넣어서 검증 준비할게
        serializer.is_valid(
            raise_exception=True
        )  # 데이터 검증하고, 실패하면 자동으로 400 에러 응답 반환할게
        #
        serializer.save()  # 검증된 데이터로 실제 User를 DB에 저장할게

        return Response(  # 처리 결과를 클라이언트에게 돌려보낼게
            {"detail": "회원가입 완료"},  # 응답 객체 안에 담을 JSON 메시지
            status=status.HTTP_201_CREATED,  # 응답상태 코드를 201(생성완료)로 설정할게
        )


# -----------------------------
# 세션 로그인 API
# -----------------------------
class SessionLoginAPIView(
    APIView
):  # APIView를 기반으로 SessionLoginAPIView 클래스 생성할게
    permission_classes = [AllowAny]  # 로그인하지 않은 사용자도 접근할 수 있어

    def post(self, request):  # post 요청이 오면 이 함수를 실행할게
        username = request.data.get(
            "username", ""
        )  # 요청 데이터에서 "username" 값을 꺼내고, 없으면 빈 문자열을 기본값으로 담아줘
        password = request.data.get(
            "password", ""
        )  # 요청 데이터에서 "password" 값을 꺼내고, 없으면 빈 문자열을 기본값으로 담아줘
        user = authenticate(
            request, username=username, password=password
        )  # username, password가 DB에 저장된 값과 일치하면 User 객체를, 실패하면 None을 담아줘

        if not user:  # authenticate()가 None을 반환했다면 (아이디/비밀번호 불일치)
            return Response(  # 사용자에게 로그인 실패 시 응답객체 반환해줘
                {
                    "detail": "아이디/비밀번호가 올바르지 않습니다."
                },  # 오류 메세지 반환해줘
                status=status.HTTP_400_BAD_REQUEST,  # 응답 상태코드를 400(잘못된 요청)으로 설정할게
            )
        login(
            request, user
        )  # 인증된 user 정보를 세션에 저장해서 로그인 상태를 유지해줘

        return Response(  # 사용자에게 로그인 성공 시 응답객체 반환해줘
            {"detail": "로그인 성공"},  # 성공 메세지 반환해줘
            status=status.HTTP_200_OK,  # 응답 상태코드를 200(성공)으로 설정할게
        )


# -----------------------------
# 세션 로그아웃 API
# -----------------------------
class SessionLogoutAPIView(
    APIView
):  # APIView를 기반으로 SessionLogoutAPIView 클래스 생성할게
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근할 수 있어

    def post(self, request):  # post 요청이 들어오면 이 함수 실행할게
        logout(request)  # 현재 사용자의 세션 데이터를 삭제해서 로그아웃 처리해줘
        return Response(  # 사용자에게 처리결과를 돌려보낼게(응답객체)
            {"detail": "로그아웃"},  # 로그아웃 메세지 반환해줘
            status=status.HTTP_200_OK,  # 응답 상태코드를 200(성공)으로 설정할게
        )
