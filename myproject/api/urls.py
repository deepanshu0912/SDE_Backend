from django.urls import path,include
from .views import RegisterView, LoginView,ProductViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]