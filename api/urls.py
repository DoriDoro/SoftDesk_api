from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views.accounts import (
    UserViewSet,
    RegisterView,
)
from .views.project import (
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)

app_name = "api"

router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="sign_up"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]


"""
router.register(r"users", UserViewSet, basename="user")
router.register(r"contributors", ContributorViewSet, basename="contributor")
router.register(r"issues", IssueViewSet, basename="issue")
router.register(r"comments", CommentViewSet, basename="comment")
"""
