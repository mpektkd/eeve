from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from eevie import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views


router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    #path('api/user/create/', views.UserViewSet.as_view(), name="create_user"),
    path('', include(router.urls)),
    path('current_user/', views.current_user),
    path('login/', views.ObtainTokenPairWithUsernameView.as_view(), name='token_create'),
    path('refreshtoken/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('healthcheck/', views.HealthCheckView.as_view(), name='healthcheck')
    #path('users/', views.UserViewSet.as_view())
    # path('article/', views.ArticleList.as_view()), #URL ./article/ is will be called
    # path('detail/<int:pk>/', views.ArticleDetail.as_view()), #URL ./detail/ is will be called with a primary key (pk)
    # path('generic/article/<int:pk>/', views.GenericAPIView.as_view()), #URL ./detail/ is will be called with a primary key (pk)
]
