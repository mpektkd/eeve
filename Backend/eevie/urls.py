from eevie.models import Car
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from eevie import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views


router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
# router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    #path('api/user/create/', views.UserViewSet.as_view(), name="create_user"),
    path('', include(router.urls)),
    path('current_user/', views.CurrentUser.as_view(), name='current_user'),
    path('login/', views.ObtainTokenPairWithUsernameView.as_view(), name='token_create'),
    path('logout/', views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='logout'),
    path('signup/', views.UserView.as_view(), name='signup'),
    path('refreshtoken/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('cars/',views.GetCars.as_view()),
    path('stations/', views.getStations.as_view()),
    path('user/payoff/', views.Payoff.as_view(),name='payoff'),
    path('user/monthlypayoff/', views.MonthlyPayoff.as_view(),name='monthlypayoff'),
    path('user/mycars/',views.MyCars.as_view()),
    path('user/mycars/chargingsession/', views.ChargingSession.as_view(),name='charging'),
    path('user/newcar/',views.InsertCar.as_view()),
    path('user/mybills/', views.MyBills.as_view()),
    path('user/mymonthlybills/', views.MyMonthlyBills.as_view()),
    path('user/deleteme/',views.DeleteMe.as_view()),
    path('admin/healthcheck/', views.HealthCheckView.as_view(), name='healthcheck'),
    path('admin/resetsessions/', views.ResetSessions.as_view()),
    path('admin/refillsessions/', views.RefillSessions.as_view()),
    path('admin/users/<str:username>/', views.InspectUser.as_view()),
    path('admin/usermod/<str:username>/<str:password>/', views.UserMod.as_view()),
    path('admin/system/sessionsupd/', views.SessionsUpd.as_view()),
    re_path(r'^SessionsPerPoint/(?P<pk>\d+)/(?P<date_from>[0-9]{8})_from/(?P<date_to>[0-9]{8})_to/$', views.SessionsPerPoint),
    re_path(r'^SessionsPerStation/(?P<pk>\d+)/(?P<date_from>[0-9]{8})_from/(?P<date_to>[0-9]{8})_to/$', views.SessionsPerStation),
    re_path(r'^SessionsPerEV/(?P<pk>\d+)/(?P<date_from>[0-9]{8})_from/(?P<date_to>[0-9]{8})_to/$', views.SessionsPerEV),
    re_path(r'^SessionsPerProvider/(?P<pk>\d+)/(?P<date_from>[0-9]{8})_from/(?P<date_to>[0-9]{8})_to/$', views.SessionsPerProvider),
    #path('users/', views.UserViewSet.as_view())/$
    # path('article/', views.ArticleList.as_view()), #URL ./article/ is will be called
    # path('detail/<int:pk>/', views.ArticleDetail.as_view()), #URL ./detail/ is will be called with a primary key (pk)
    # path('generic/article/<int:pk>/', views.GenericAPIView.as_view()), #URL ./detail/ is will be called with a primary key (pk)
]
#SessionsPerPoint/263271/20190901_from/20200803_to