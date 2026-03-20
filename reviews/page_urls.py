from django.urls import path
from . import views

urlpatterns = [
    path("page/", views.reviews_page, name="reviews-page"),
]
