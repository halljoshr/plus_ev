from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("fetch_data/", views.fetch_data, name="fetch_data"),
    # path("fetch-data/", views.FetchData.as_view(), name="fetch_data"),
    # path("fetch_data/", views.AsyncFetchData.as_view(), name="fetch_data"),
    path("get_posts/", views.get_posts, name="get_posts"),
    path("save_bet/", views.save_bet, name="save_bet"),
]
