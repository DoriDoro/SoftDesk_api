from django.urls import path, include
from rest_framework import routers

from .views.accounts import UserAPIView
from .views.project import (
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)

app_name = "api"

router = routers.DefaultRouter()
# router.register(r"users", UserAPIView, basename="user")
router.register(r"contributors", ContributorViewSet, basename="contributor")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"issues", IssueViewSet, basename="issue")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    # path("", UserAPIView.as_view(), name="home"),
]
