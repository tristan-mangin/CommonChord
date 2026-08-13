from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    path("repos/", views.RepositoryListView.as_view(), name="repo-list"),
    path("repos/<int:repo_id>/", views.RepositoryDetailView.as_view(), name="repo-detail"),
    path("repos/<int:repo_id>/commits/", views.CommitListView.as_view(), name="commit-list"),
    path("repos/<int:repo_id>/add/", views.StageFileView.as_view(), name="stage-file"),
    path("repos/<int:repo_id>/checkout/<str:commit_hash>/", views.CheckoutView.as_view(), name="checkout"),
    path("repos/<int:repo_id>/status/", views.StatusView.as_view(), name="status"),
    path("repos/<int:repo_id>/commits/<str:commit_hash>/als/", views.ParseALSView.as_view(), name="als-parser"),
    path("repos/<int:repo_id>/commits/<str:commit_hash>/waveform/", views.WaveformView.as_view(), name="waveform"),
    path("auth/register/", auth_views.RegisterView.as_view(), name="register"),
    path("auth/login/", auth_views.LoginView.as_view(), name="login"),
    path("auth/logout/", auth_views.LogoutView.as_view(), name="logout"),
]
