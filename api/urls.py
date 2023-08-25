from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.accounts import UserAPIView, MyObtainTokenPairView
from .views.project import (
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)

app_name = "api"

router = routers.DefaultRouter()
# router.register(r"users", UserViewSet, basename="user")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"contributors", ContributorViewSet, basename="contributor")
router.register(r"issues", IssueViewSet, basename="issue")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("", UserAPIView.as_view(), name="home"),
]
