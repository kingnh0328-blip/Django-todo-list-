from pathlib import Path
import os
import environ  # environ = 환경변수 추가

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 보안 향상, 코드 재사용, 환경 구분 가능
env = environ.Env(DEBUG=(bool, False))

# 환경변수
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY를 .env로 이동하여 보호
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "todo",
    "rest_framework",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.AllowAny", 기본권한 설정: 누구나 API에 접근 가능(개발시 사용)
        # "rest_framework.authentication.SessionAuthentication",  # 세션 인증 (Django 로그인 기반): 브라우저에서 로그인 상태라면 자동 인증됨
        # "rest_framework.authentication.BasicAuthentication",  # Basic 인증 (아이디/비밀번호 헤더로 보내는 방식): 주로 테스트용으로 사용됨 (Postman, curl 등)
        "rest_framework.permissions.IsAuthenticated",  # 로그인한 사용자만 API 사용 가능
    ],
    "DEFAULT_PAGINATION_CLASS": "todo.pagination.CustomPageNumberPagination",  # 기본 페이지네이션 클래스 설정: API 목록 조회 시 페이지 단위로 데이터를 반환
    "PAGE_SIZE": 3,  # 기본 페이지 크기: 한 페이지에 3개씩 출력하겠다는 의미, 아무것도 설정하지 않으면 디폴트 = 10
    # 응답 데이터 출력 형식(Renderer)
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",  # JSON 형식 응답(프론트앤드 / API 사용 시 기본)
        # "rest_framework.renderers.BrowsableAPIRenderer",  # DRF 브라우저 API 화면 제공 (개발/테스트용)
    ],
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
