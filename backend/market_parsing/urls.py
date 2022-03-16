from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.SimpleRouter()

router.register(r'user', views.UserViewSet)
router.register(r'password', views.ChangePasswordView)

urlpatterns = [
    path("", include(router.urls)),
    path('link/', views.LinkView.as_view({'get': 'list', 'post': 'create'})),
    path('link/<int:pk>/', views.LinkView.as_view({'put': 'update', 'delete': 'destroy'})),
    
    path('update_profile/', views.UpdateProfileView.as_view(), name='auth_update_profile'),
    
    path("token/", views.TokenGet.as_view(), name="token_get"),
    
    path("check_email/", views.CheckEmail.as_view(), name="check_email"),
    path("check_token/", views.CheckToken.as_view(), name="check_token"),
]
