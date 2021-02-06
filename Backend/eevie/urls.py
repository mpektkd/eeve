from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from eevie import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('customer', views.CustomerViewSet, basename='customer')

urlpatterns = [
    path('customer/', include(router.urls)),
    path('customer/<int:pk>/', include(router.urls)),
    # path('article/', views.ArticleList.as_view()), #URL ./article/ is will be called
    # path('detail/<int:pk>/', views.ArticleDetail.as_view()), #URL ./detail/ is will be called with a primary key (pk)
    # path('generic/article/<int:pk>/', views.GenericAPIView.as_view()), #URL ./detail/ is will be called with a primary key (pk)
]
